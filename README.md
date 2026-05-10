# SHL Assessment Recommender

A conversational AI chatbot that helps hiring managers find the right SHL assessment tests for their job roles. Instead of manually searching through catalogs, users can simply chat with the bot to get personalized recommendations.

## 🚀 Quick Start

### Option 1: Use the startup script (Windows)
```bash
# Double-click or run:
start_server.bat
```

### Option 2: Manual startup
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Run demo
```bash
# Start server first, then in another terminal:
python demo.py
```

## 🎯 What It Does

The bot intelligently:
- **Asks follow-up questions** if your query is vague
- **Recommends 1-10 tests** once it understands your needs
- **Updates recommendations** if you change requirements mid-chat
- **Compares assessments** when asked
- **Refuses off-topic** questions politely

## 💬 Example Conversations

**Vague Query:**
```
User: "I need an assessment"
Bot: "What role are you hiring for?"
```

**Specific Query:**
```
User: "Mid-level Java developer with 4 years experience"
Bot: "Here are 5 Java assessments for mid-level developers:
      1. Java 8 (New) - Knowledge & Skills
      2. Core Java (Advanced Level) - Knowledge & Skills
      ..."
```

**Multi-turn:**
```
User: "I need to hire a developer"
Bot: "What programming language?"
User: "Python"
Bot: "What seniority level?"
User: "Senior with data science experience"
Bot: "Here are Python and data science assessments..."
```

## 🔧 API Endpoints

### GET /health
Health check endpoint.
```json
{"status": "ok"}
```

### POST /chat
Main chat endpoint. Accepts conversation history and returns response with recommendations.

**Request Schema:**
```json
{
  "messages": [
    {"role": "user", "content": "string"},
    {"role": "assistant", "content": "string"}
  ]
}
```

**Response Schema:**
```json
{
  "reply": "string",
  "recommendations": [
    {
      "name": "Assessment Name",
      "url": "https://www.shl.com/products/...",
      "test_type": "K|P|A|S"
    }
  ],
  "end_of_conversation": boolean
}
```

**Test Types:**
- `K` = Knowledge & Skills
- `P` = Personality & Behavior  
- `A` = Ability & Aptitude
- `S` = Simulations

## 🧪 Testing

### HTTP Tests (VS Code REST Client)
Use `test_main.http` with the REST Client extension.

### Python Tests
```bash
# Comprehensive test suite
python test_comprehensive.py

# Basic API tests
python test_api.py
```

### Manual Testing
```bash
# Health check
curl http://localhost:8000/health

# Chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Java developer assessment"}]}'
```

## 🏗️ Architecture

### Tech Stack
- **FastAPI** - Web framework
- **Google Gemini** - LLM for intent understanding
- **Python** - Backend language
- **JSON** - Data storage (1000+ SHL assessments)

### How It Works
1. **Intent Parsing**: Gemini analyzes user messages to extract:
   - Job role (developer, manager, etc.)
   - Technology stack (Java, Python, etc.)
   - Seniority level (junior, mid, senior)
   - Skills needed (technical, soft skills)

2. **Smart Search**: Keyword-based scoring system matches:
   - Technical skills (high weight)
   - Soft skills (medium weight)
   - Job levels (contextual weight)
   - Assessment types (preference-based)

3. **Response Generation**: Returns structured JSON with:
   - Natural language reply
   - Ranked assessment recommendations
   - Conversation state

### Key Features
- **Stateless Design**: Each request contains full conversation history
- **Graceful Degradation**: Fallback responses if AI fails
- **Schema Validation**: Pydantic models ensure data integrity
- **Rate Limiting Ready**: Designed for production deployment

## 📊 Assessment Catalog

The bot has access to **1000+ SHL assessments** including:
- **Programming Languages**: Java, Python, JavaScript, C#, C++, etc.
- **Frameworks**: Spring, React, Angular, Node.js, etc.
- **Technologies**: Docker, Kubernetes, AWS, databases, etc.
- **Soft Skills**: Communication, leadership, customer service
- **Industries**: Healthcare, finance, manufacturing, etc.
- **Job Levels**: Entry-level to executive

## 🚀 Deployment

### Render (Recommended)
1. Fork this repo
2. Connect to Render
3. Set environment variable: `GEMINI_KEY`
4. Deploy automatically

### Railway
1. Connect GitHub repo
2. Add `GEMINI_KEY` environment variable
3. Auto-deploys on push

### Fly.io
```bash
fly launch
fly secrets set GEMINI_KEY=your_key
fly deploy
```

### Docker
```bash
docker build -t shl-recommender .
docker run -p 8000:8000 -e GEMINI_KEY=your_key shl-recommender
```

## 🔑 Environment Variables

```bash
# Required
GEMINI_KEY=your_gemini_api_key_here

# Optional
PORT=8000  # For deployment platforms
```

## 🎯 Design Decisions

1. **Gemini over OpenAI**: Free tier, generous limits, good performance
2. **Keyword Search over Vector DB**: Simpler, faster, sufficient for this use case
3. **JSON Catalog over Database**: Faster cold starts, easier deployment
4. **Stateless API**: Easier to scale, no session management
5. **Minimal Dependencies**: Faster deployments, lower costs

## 📈 Performance

- **Response Time**: < 5 seconds typical, < 30 seconds max
- **Accuracy**: High precision for specific queries
- **Scalability**: Stateless design supports horizontal scaling
- **Reliability**: Fallback responses ensure uptime

## 🔍 Evaluation Metrics

- **Recall@10**: Measures if relevant assessments are in top 10
- **Turn Efficiency**: Minimizes questions needed
- **Schema Compliance**: 100% valid JSON responses
- **Response Time**: < 30 seconds per request
- **Conversation Handling**: Up to 8 turns supported

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.