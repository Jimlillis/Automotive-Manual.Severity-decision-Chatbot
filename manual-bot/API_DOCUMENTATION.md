# API Documentation

Complete API reference for the Automotive Manual ChatBot.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. For production, implement token-based auth.

## Response Format

All responses are JSON formatted with appropriate HTTP status codes.

### Success Response (200)
```json
{
  "data": "...",
  "status": "success"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

---

## Endpoints

### Health & Status

#### GET `/`
Root endpoint - basic information.

**Response:**
```json
{
  "name": "Automotive Manual ChatBot",
  "version": "1.0.0",
  "status": "running"
}
```

---

#### GET `/health`
System health check.

**Response:**
```json
{
  "status": "healthy",
  "message": "System is operational",
  "ready": true
}
```

**Status Codes:**
- `200`: System healthy
- `500`: System unhealthy

---

#### GET `/config`
Get current system configuration (non-sensitive).

**Response:**
```json
{
  "app_name": "Automotive Manual ChatBot",
  "version": "1.0.0",
  "model": "gpt-4",
  "chunk_size": 1024,
  "chunk_overlap": 100,
  "top_k_chunks": 5,
  "temperature": 0.7,
  "max_tokens": 1000
}
```

---

### Question Answering

#### POST `/ask`
Ask a question about vehicle manuals. The system will retrieve relevant sections and generate an answer.

**Request:**
```json
{
  "question": "How do I change the oil?",
  "top_k": 5
}
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| question | string | Yes | The question to ask |
| top_k | integer | No | Number of chunks to retrieve (default: 5) |

**Response (200):**
```json
{
  "answer": "To change the oil, first warm up the engine...",
  "sources": "Sources: Page 42, Page 45",
  "retrieved_chunks": 3,
  "model": "gpt-4",
  "tokens_used": 287
}
```

**Response (400):**
```json
{
  "detail": "Question cannot be empty"
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I change the oil?",
    "top_k": 5
  }'
```

**Python Example:**
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={
        "question": "How do I change the oil?",
        "top_k": 5
    }
)
answer = response.json()
print(answer["answer"])
print(answer["sources"])
```

---

#### GET `/retrieve`
Search for relevant documents without generating an answer. Useful for debugging.

**Query Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| query | string | Yes | Search query |
| top_k | integer | No | Number of results (default: 5) |

**Response (200):**
```json
{
  "query": "tire pressure",
  "retrieved_count": 3,
  "documents": [
    {
      "content": "The recommended tire pressure is 32 PSI...",
      "page": 12,
      "distance": 0.15
    },
    {
      "content": "Check tire pressure monthly...",
      "page": 15,
      "distance": 0.22
    }
  ]
}
```

**Curl Example:**
```bash
curl "http://localhost:8000/retrieve?query=tire%20pressure&top_k=5"
```

**Python Example:**
```python
import requests

response = requests.get(
    "http://localhost:8000/retrieve",
    params={
        "query": "tire pressure",
        "top_k": 5
    }
)
docs = response.json()
for doc in docs["documents"]:
    print(f"Page {doc['page']}: {doc['content'][:100]}...")
```

---

### Manual Management

#### POST `/upload-manual`
Upload a vehicle manual PDF file.

**Request:**
Multipart form data with file upload

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| file | file | Yes | PDF file to upload |

**Response (200):**
```json
{
  "filename": "toyota_camry_2023.pdf",
  "size": 12845678,
  "message": "File toyota_camry_2023.pdf uploaded successfully. Use /ingest to add to knowledge base."
}
```

**Curl Example:**
```bash
curl -X POST -F "file=@manual.pdf" http://localhost:8000/upload-manual
```

**Python Example:**
```python
import requests

with open("manual.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/upload-manual",
        files=files
    )
    print(response.json()["message"])
```

---

#### POST `/ingest`
Ingest all PDF manuals from the `data/manuals/` directory. This processes them and adds to the vector database.

**Request:**
No body required.

**Response (200):**
```json
{
  "documents_ingested": 1250,
  "message": "Successfully ingested 1250 document chunks"
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/ingest
```

**Python Example:**
```python
import requests

response = requests.post("http://localhost:8000/ingest")
result = response.json()
print(f"Ingested {result['documents_ingested']} chunks")
```

---

#### DELETE `/clear-database`
Clear the vector database. **WARNING**: This deletes all ingested documents!

**Request:**
No body required.

**Response (200):**
```json
{
  "status": "success",
  "message": "Vector database cleared successfully"
}
```

**Curl Example:**
```bash
curl -X DELETE http://localhost:8000/clear-database
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

---

## Error Handling

### Example Error Response

**Request:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": ""}'
```

**Response (400):**
```json
{
  "detail": "Question cannot be empty",
  "status_code": 400
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, implement:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/ask")
@limiter.limit("30/minute")
async def ask_question(request: QuestionRequest):
    ...
```

---

## Pagination

Not implemented yet. For future use with large result sets:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total": 100,
    "total_pages": 10
  }
}
```

---

## Webhooks

Not implemented. Future feature for async notifications.

---

## Batch Requests

Not implemented. For processing multiple requests efficiently.

---

## WebSocket Support

Not implemented. Future feature for real-time chat.

---

## API Versioning

Current version: `1.0.0` (no versioning yet)

For future versions: `/api/v2/ask`

---

## CORS Headers

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type
```

---

## Examples

### Complete Integration Example

```python
import requests
import json

class ChatbotClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self):
        """Check if system is healthy"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def upload_manual(self, filepath):
        """Upload a manual"""
        with open(filepath, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{self.base_url}/upload-manual",
                files=files
            )
        return response.json()
    
    def ingest_manuals(self):
        """Ingest all manuals"""
        response = requests.post(f"{self.base_url}/ingest")
        return response.json()
    
    def ask_question(self, question, top_k=5):
        """Ask a question"""
        response = requests.post(
            f"{self.base_url}/ask",
            json={"question": question, "top_k": top_k}
        )
        return response.json()
    
    def search(self, query, top_k=5):
        """Search documents"""
        response = requests.get(
            f"{self.base_url}/retrieve",
            params={"query": query, "top_k": top_k}
        )
        return response.json()

# Usage
client = ChatbotClient()

# Check health
print(client.health_check())

# Upload and ingest
client.upload_manual("manual.pdf")
client.ingest_manuals()

# Ask a question
answer = client.ask_question("How do I change the oil?")
print(answer["answer"])
print(answer["sources"])

# Search
results = client.search("tire pressure")
for doc in results["documents"]:
    print(f"Page {doc['page']}: {doc['content'][:100]}")
```

---

## Change Log

### Version 1.0.0 (March 2026)
- Initial release
- RAG system with PDF processing
- FastAPI backend
- Web UI frontend
- Vector database (Chroma)
- OpenAI integration
