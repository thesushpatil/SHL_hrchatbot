# API Examples

## Health Check

### Request
```bash
GET http://localhost:8000/health
```

### Response
```json
{
  "status": "ok"
}
```

---

## Example 1: Vague Query (Should Clarify)

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "I need an assessment"
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "What role are you hiring for?",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

## Example 2: Specific Query (Should Recommend)

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "I'm hiring a mid-level Java developer with 4 years experience"
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "Here are 5 assessments for a mid-level Java developer...",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/products/product-catalog/view/java-8-new/",
      "test_type": "K"
    },
    {
      "name": "Core Java (Advanced Level) (New)",
      "url": "https://www.shl.com/products/product-catalog/view/core-java-advanced-level-new/",
      "test_type": "K"
    }
  ],
  "end_of_conversation": true
}
```

---

## Example 3: Multi-turn Conversation

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "I need to hire a developer"
    },
    {
      "role": "assistant",
      "content": "What programming language or technology?"
    },
    {
      "role": "user",
      "content": "Java"
    },
    {
      "role": "assistant",
      "content": "What seniority level?"
    },
    {
      "role": "user",
      "content": "Mid-level, around 4 years"
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "Here are assessments for a mid-level Java developer...",
  "recommendations": [...],
  "end_of_conversation": true
}
```

---

## Example 4: Job Description

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "Here is a job description: We need a Senior Java Developer with Spring Boot experience who will work closely with stakeholders and lead a small team."
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "Based on the job description, here are assessments...",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/...",
      "test_type": "K"
    },
    {
      "name": "OPQ32r",
      "url": "https://www.shl.com/...",
      "test_type": "P"
    }
  ],
  "end_of_conversation": true
}
```

---

## Example 5: Refinement

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "I need assessments for a Java developer"
    },
    {
      "role": "assistant",
      "content": "Here are Java assessments..."
    },
    {
      "role": "user",
      "content": "Actually, add personality tests too"
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "Updated recommendations with personality tests...",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/...",
      "test_type": "K"
    },
    {
      "name": "OPQ32r",
      "url": "https://www.shl.com/...",
      "test_type": "P"
    }
  ],
  "end_of_conversation": true
}
```

---

## Example 6: Comparison

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "What is the difference between OPQ and GSA?"
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "Comparing OPQ32r and Global Skills Assessment:\n\nOPQ32r: A personality assessment...\n\nGlobal Skills Assessment: Measures 96 discrete skills...",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

## Example 7: Off-Topic (Should Refuse)

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "What's the weather today?"
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "I can only help with SHL assessment recommendations. Is there an assessment you'd like to know about?",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

## Example 8: Python Developer

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "Python developer, entry level"
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "Here are assessments for an entry-level Python developer...",
  "recommendations": [
    {
      "name": "Python Programming (New)",
      "url": "https://www.shl.com/...",
      "test_type": "K"
    }
  ],
  "end_of_conversation": true
}
```

---

## Example 9: Leadership Role

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "I need assessments for a senior manager position"
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "Here are assessments for a senior manager...",
  "recommendations": [
    {
      "name": "Management Scenarios",
      "url": "https://www.shl.com/...",
      "test_type": "P"
    },
    {
      "name": "Executive Scenarios",
      "url": "https://www.shl.com/...",
      "test_type": "P"
    }
  ],
  "end_of_conversation": true
}
```

---

## Example 10: Customer Service

### Request
```bash
POST http://localhost:8000/chat
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "Entry-level customer service representative"
    }
  ]
}
```

### Expected Response
```json
{
  "reply": "Here are assessments for an entry-level customer service role...",
  "recommendations": [
    {
      "name": "Customer Service Phone Solution",
      "url": "https://www.shl.com/...",
      "test_type": "S"
    },
    {
      "name": "Entry Level Customer Service (General) Solution",
      "url": "https://www.shl.com/...",
      "test_type": "P"
    }
  ],
  "end_of_conversation": true
}
```

---

## Test Types

- **K**: Knowledge & Skills
- **P**: Personality & Behavior
- **A**: Ability & Aptitude
- **S**: Simulations

---

## cURL Commands

### Health Check
```bash
curl http://localhost:8000/health
```

### Simple Chat
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Java developer assessment"}]}'
```

### Pretty Print Response
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Java developer"}]}' \
  | python -m json.tool
```

---

## PowerShell Commands (Windows)

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

### Chat Request
```powershell
$body = @{
    messages = @(
        @{
            role = "user"
            content = "Java developer assessment"
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
```
