from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Load catalog using strict=False to handle control characters
try:
    with open("shl_product_catalog.json", "r", encoding="utf-8") as f:
        CATALOG = json.loads(f.read(), strict=False)
except Exception as e:
    print(f"Error loading catalog: {e}")
    CATALOG = []

# Build search index
INDEX = []
for item in CATALOG:
    text = f"{item['name']} {item.get('description','')} {' '.join(item.get('keys', []))} {' '.join(item.get('job_levels', []))}"
    INDEX.append({"item": item, "text": text.lower()})


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool


def extract_test_type(item):
    keys = item.get("keys", [])
    if "Knowledge & Skills" in keys:
        return "K"
    elif "Personality & Behavior" in keys:
        return "P"
    elif "Ability & Aptitude" in keys:
        return "A"
    elif "Simulations" in keys:
        return "S"
    return "K"


def search_assessments(query: str, context: dict) -> List[dict]:
    query_lower = query.lower()
    scored = []

    tech_skills = ["java", "python", "javascript", "c#", "sql", "testing", "agile", "cloud", "aws",
                   "data", "angular", "react", "node", "docker", "kubernetes", ".net", "c++", "ruby",
                   "scala", "go", "swift", "kotlin", "php", "r ", "machine learning", "devops"]
    soft_skills = ["personality", "leadership", "communication", "customer service", "sales",
                   "management", "teamwork", "problem solving", "critical thinking"]

    for entry in INDEX:
        score = 0
        text = entry["text"]
        item = entry["item"]

        for skill in tech_skills:
            if skill in query_lower and skill in text:
                score += 10

        for skill in soft_skills:
            if skill in query_lower and skill in text:
                score += 8

        if context.get("seniority"):
            level = context["seniority"].lower()
            if level in text:
                score += 5

        if "senior" in query_lower or "experienced" in query_lower:
            if "mid-professional" in text or "professional individual contributor" in text:
                score += 3
        elif "junior" in query_lower or "entry" in query_lower or "graduate" in query_lower:
            if "entry-level" in text or "graduate" in text:
                score += 3

        if "developer" in query_lower and "knowledge & skills" in text:
            score += 2
        if "manager" in query_lower and ("manager" in text or "leadership" in text):
            score += 3
        if "personality" in query_lower and "personality & behavior" in text:
            score += 3

        # Word-level general matching
        for word in query_lower.split():
            if len(word) > 3 and word in text:
                score += 1

        if score > 0:
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [item for _, item in scored[:10]]


def fuzzy_find_assessments(names: List[str]) -> List[dict]:
    """Find assessments by partial/fuzzy name match."""
    results = []
    for name in names:
        name_lower = name.lower()
        best = None
        best_score = 0
        for item in CATALOG:
            item_name_lower = item["name"].lower()
            # Score by how many words from the search name appear in the catalog name
            words = [w for w in name_lower.split() if len(w) > 2]
            score = sum(1 for w in words if w in item_name_lower)
            if score > best_score:
                best_score = score
                best = item
        if best and best_score > 0:
            results.append(best)
    return results


def build_prompt(messages: List[Message]) -> str:
    conversation = "\n".join([f"{m.role}: {m.content}" for m in messages])
    return f"""You are an SHL assessment recommender assistant helping hiring managers select the right assessments.

RULES:
1. ONLY discuss SHL assessments - refuse all off-topic questions politely
2. If the query is vague (missing role, seniority, or skills), ask ONE clarifying question
3. Once you have: role + (seniority OR skills), recommend assessments
4. For comparisons, identify the assessment names being compared
5. If user refines or changes requirements, action must be "recommend" again with updated query
6. Be concise and professional

CONVERSATION:
{conversation}

Respond with ONLY a JSON object (no markdown, no extra text):
{{
  "action": "clarify" | "recommend" | "refuse" | "compare",
  "reply": "your response to the user",
  "query": "search terms for finding assessments (only if action=recommend)",
  "names": ["assessment1", "assessment2"] (only if action=compare)
}}

Examples:
- Vague: "I need an assessment" → action: "clarify", reply: "What role are you hiring for?"
- Specific: "Java developer, mid-level" → action: "recommend", query: "java developer mid-level knowledge skills"
- Refinement: "Actually make it senior level" → action: "recommend", query: "java developer senior"
- Off-topic: "What's the weather?" → action: "refuse", reply: "I can only help with SHL assessments."
- Compare: "Difference between OPQ and MQ?" → action: "compare", names: ["OPQ32r", "Motivation Questionnaire"]
"""


def call_gemini(prompt: str) -> dict:
    api_key = os.getenv("GEMINI_KEY")
    if not api_key:
        return {"action": "clarify", "reply": "API key not configured.", "query": ""}

    try:
        client = genai.Client(api_key=api_key)
        model = "gemini-flash-latest"
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=1000)
        )
        
        text = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Gemini error: {e}")
        return {"action": "clarify", "reply": "Service temporarily unavailable. Please try again.", "query": ""}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        full_text = " ".join([m.content for m in request.messages if m.role == "user"]).lower()

        context = {"seniority": None}
        if "senior" in full_text or "experienced" in full_text:
            context["seniority"] = "mid-professional"
        elif "junior" in full_text or "entry" in full_text or "graduate" in full_text:
            context["seniority"] = "entry-level"

        result = call_gemini(build_prompt(request.messages))
        action = result.get("action", "clarify")
        reply = result.get("reply", "")
        recommendations = []

        if action == "recommend":
            query = result.get("query", full_text)
            items = search_assessments(query, context)
            recommendations = [
                Recommendation(name=item["name"], url=item["link"], test_type=extract_test_type(item))
                for item in items
            ]

        elif action == "compare":
            names = result.get("names", [])
            items = fuzzy_find_assessments(names)
            if len(items) >= 2:
                reply = f"Comparing **{items[0]['name']}** and **{items[1]['name']}**:\n\n"
                reply += f"**{items[0]['name']}**: {items[0].get('description', 'No description available.')}\n\n"
                reply += f"**{items[1]['name']}**: {items[1].get('description', 'No description available.')}"
                recommendations = [
                    Recommendation(name=item["name"], url=item["link"], test_type=extract_test_type(item))
                    for item in items[:2]
                ]
            elif len(items) == 1:
                reply = f"Found **{items[0]['name']}** but could not find the second assessment. Please clarify the name."

        # end_of_conversation is always false to allow refinement
        return ChatResponse(reply=reply, recommendations=recommendations, end_of_conversation=False)

    except Exception as e:
        return ChatResponse(
            reply="I encountered an error. Could you rephrase your question?",
            recommendations=[],
            end_of_conversation=False
        )
