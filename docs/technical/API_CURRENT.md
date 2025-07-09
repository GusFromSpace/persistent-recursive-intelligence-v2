# Mesopredator PRI - Current API Documentation

**Version:** 1.0.0 (Basic Implementation)  
**Status:** Development/Local Use  
**Authentication:** None implemented  
**Base URL:** http://localhost:8000

---

## 🚨 **IMPORTANT NOTICE**

This documentation reflects the **actual current implementation** as of 2025-07-03. This is a basic API with 8 endpoints designed for local development and simple integration. 

**This API does NOT include:**
- Authentication/authorization
- WebSocket support
- Advanced features described in API_COMPREHENSIVE.md
- Production security features
- Rate limiting
- Team collaboration features

---

## 🚀 Quick Start

```bash
# Start the API server
cd /home/gusfromspace/Development/persistent-recursive-intelligence
python -m src.api.rest.simple_api

# API will be available at:
# - Main: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

---

## 📋 Available Endpoints

### 1. Health Check
```http
GET /health
```

**Description:** Check API and system health  
**Authentication:** None required  

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-03T17:00:00Z",
  "components": {
    "database": "healthy",
    "vector_search": "healthy", 
    "memory_count": 150,
    "namespace": "default"
  },
  "api_version": "1.0.0"
}
```

---

### 2. Memory Operations

#### Store Memory
```http
POST /api/v1/memory/store
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "Recursive improvement pattern: always validate input before processing",
  "metadata": {
    "type": "pattern",
    "project": "example-project",
    "category": "improvement"
  }
}
```

**Response:**
```json
{
  "memory_id": 123,
  "status": "stored"
}
```

#### Search Memories
```http
POST /api/v1/memory/search
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "optimization patterns",
  "limit": 10,
  "similarity_threshold": 0.5
}
```

**Response:**
```json
{
  "memories": [
    {
      "id": 123,
      "content": "Recursive improvement pattern: always validate input before processing",
      "metadata": {
        "type": "pattern",
        "project": "example-project"
      },
      "timestamp": 1719057000.0,
      "search_type": "semantic"
    }
  ],
  "total_count": 1,
  "query": "optimization patterns"
}
```

---

### 3. Intelligence Operations

#### Evolve Intelligence
```http
POST /api/v1/intelligence/evolve
Content-Type: application/json
```

**Request Body:**
```json
{
  "project_path": "/path/to/project",
  "max_iterations": 3
}
```

**Response:**
```json
{
  "status": "completed",
  "results": {
    "session_id": "session_20250703_170000",
    "project_path": "/path/to/project",
    "iterations_completed": 3,
    "improvements_applied": [],
    "new_patterns_discovered": [],
    "emergent_insights": []
  }
}
```

#### Transfer Patterns
```http
POST /api/v1/intelligence/transfer
Content-Type: application/json
```

**Request Body:**
```json
{
  "source_projects": ["/path/to/project1", "/path/to/project2"],
  "target_project": "/path/to/new/project"
}
```

**Response:**
```json
{
  "status": "completed",
  "results": {
    "source_projects": ["/path/to/project1", "/path/to/project2"],
    "target_project": "/path/to/new/project",
    "patterns_transferred": [],
    "adaptations_made": []
  }
}
```

---

### 4. System Operations

#### Get System Statistics
```http
GET /api/v1/system/stats
```

**Response:**
```json
{
  "memory_count": 150,
  "health": {
    "database": "healthy",
    "vector_search": "healthy",
    "memory_count": 150,
    "namespace": "default"
  },
  "timestamp": "2025-07-03T17:00:00Z"
}
```

#### Clear System
```http
DELETE /api/v1/system/clear
```

⚠️ **Warning:** Clears all stored memories. Use with caution.

**Response:**
```json
{
  "status": "cleared",
  "message": "All memories cleared"
}
```

---

## 💻 Usage Examples

### Python Example
```python
import requests

# Store a memory
response = requests.post("http://localhost:8000/api/v1/memory/store", json={
    "content": "Always validate input parameters before processing",
    "metadata": {"type": "best_practice", "language": "python"}
})
print(response.json())  # {"memory_id": 123, "status": "stored"}

# Search memories
response = requests.post("http://localhost:8000/api/v1/memory/search", json={
    "query": "validation patterns",
    "limit": 5
})
memories = response.json()["memories"]

# Evolve intelligence on a project
response = requests.post("http://localhost:8000/api/v1/intelligence/evolve", json={
    "project_path": "/home/user/my-project",
    "max_iterations": 2
})
results = response.json()["results"]
```

### JavaScript Example
```javascript
// Store a memory
const storeResponse = await fetch('http://localhost:8000/api/v1/memory/store', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        content: "Use async/await for better error handling",
        metadata: { type: "pattern", language: "javascript" }
    })
});
const stored = await storeResponse.json();

// Search memories
const searchResponse = await fetch('http://localhost:8000/api/v1/memory/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        query: "error handling",
        limit: 10
    })
});
const searchResults = await searchResponse.json();
```

### cURL Examples
```bash
# Health check
curl http://localhost:8000/health

# Store memory
curl -X POST "http://localhost:8000/api/v1/memory/store" \
     -H "Content-Type: application/json" \
     -d '{"content": "Security pattern: use parameterized queries", "metadata": {"type": "security"}}'

# Search memories
curl -X POST "http://localhost:8000/api/v1/memory/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "security patterns", "limit": 5}'

# Get system stats
curl http://localhost:8000/api/v1/system/stats
```

---

## ⚠️ Error Handling

### Standard Error Response
```json
{
  "error": "Validation Error",
  "detail": "Invalid project path: /nonexistent/path"
}
```

### HTTP Status Codes
- `200` - Success
- `400` - Validation Error (bad request data)
- `500` - Internal Server Error

---

## 🔧 Configuration

### Environment Variables
```bash
# No authentication configured
# No rate limiting implemented
# No advanced configuration options

# Basic FastAPI settings work:
export UVICORN_HOST=0.0.0.0
export UVICORN_PORT=8000
```

### Dependencies
```bash
pip install fastapi uvicorn
# Memory system dependencies:
pip install sqlite3  # built-in
pip install faiss-cpu  # for semantic search
pip install sentence-transformers  # for embeddings
```

---

## 🚧 Current Limitations

### What's Missing
- **Authentication**: No API keys, no user management
- **Authorization**: No access control or permissions
- **Rate Limiting**: No request throttling
- **Validation**: Minimal input validation
- **Logging**: Basic error logging only
- **Monitoring**: No metrics or health monitoring
- **Security**: No HTTPS, no security headers
- **Documentation**: Request/response models not fully defined

### Performance Considerations
- **Single Process**: No horizontal scaling
- **Memory Usage**: All data loaded in memory
- **Concurrent Requests**: Basic FastAPI concurrency only
- **Database**: SQLite for development use only

---

## 🎯 Production Readiness

**Current Status: NOT PRODUCTION READY**

### Required for Production
- [ ] Authentication system
- [ ] Input validation and sanitization
- [ ] Rate limiting
- [ ] Proper error handling
- [ ] Security headers
- [ ] HTTPS support
- [ ] Database connection pooling
- [ ] Logging and monitoring
- [ ] Health checks for dependencies
- [ ] Graceful shutdown handling

---

## 📈 Roadmap

### Next Version (1.1.0)
- API key authentication
- Input validation with Pydantic models
- Proper error responses
- Basic rate limiting

### Future Versions
- WebSocket support for real-time updates
- Advanced authentication (OAuth, JWT)
- Role-based access control
- Comprehensive monitoring
- SDK development

---

## 🔍 Testing the API

### Manual Testing
```bash
# Start the server
python -m src.api.rest.simple_api

# Test health endpoint
curl http://localhost:8000/health

# View interactive docs
open http://localhost:8000/docs
```

### Automated Testing
```python
import pytest
import requests

def test_health_endpoint():
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_store_memory():
    response = requests.post(
        "http://localhost:8000/api/v1/memory/store",
        json={"content": "test memory", "metadata": {}}
    )
    assert response.status_code == 200
    assert "memory_id" in response.json()
```

---

**This API documentation accurately reflects the current implementation. For the full-featured API described in other documentation, see the roadmap and development plans.**