# Persistent Recursive Intelligence API

Simple REST API for external programs to interact with the persistent recursive intelligence system.

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check
```http
GET /health
```
Returns system health status and component information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-22T10:30:00Z",
  "components": {
    "database": "healthy",
    "vector_search": "healthy",
    "memory_count": 150,
    "namespace": "default"
  },
  "api_version": "1.0.0"
}
```

### Memory Operations

#### Store Memory
```http
POST /api/v1/memory/store
```
Store new information in the memory system.

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
```
Search stored memories using semantic or text search.

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

### Intelligence Operations

#### Evolve Intelligence
```http
POST /api/v1/intelligence/evolve
```
Run persistent recursive intelligence evolution on a project.

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
    "session_id": "session_20250622_103000",
    "project_path": "/path/to/project",
    "iterations_completed": 3,
    "improvements_applied": [...],
    "new_patterns_discovered": [...],
    "emergent_insights": [...]
  }
}
```

#### Transfer Patterns
```http
POST /api/v1/intelligence/transfer
```
Transfer learned patterns from source projects to target project.

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
    "patterns_transferred": [...],
    "adaptations_made": [...]
  }
}
```

### System Operations

#### Get System Statistics
```http
GET /api/v1/system/stats
```
Get current system statistics and health information.

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
  "timestamp": "2025-06-22T10:30:00Z"
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

## Usage Examples

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

## Running the API

### Start the Server
```bash
cd /home/gusfromspace/Development/persistent-recursive-intelligence
python -m src.api.rest.simple_api
```

The API will be available at `http://localhost:8000` with automatic documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Requirements
The API requires the following dependencies:
- `fastapi`
- `uvicorn`
- `sqlite3` (built-in)
- `faiss-cpu` or `faiss-gpu` (optional, for semantic search)
- `sentence-transformers` (optional, for semantic search)

Install with:
```bash
pip install fastapi uvicorn faiss-cpu sentence-transformers
```