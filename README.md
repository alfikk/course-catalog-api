# Course Catalog API

REST API for a university course catalog built with **FastAPI** and **Pydantic**.  
Provides filtering, sorting, and pagination over a list of six courses.

## How to run

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\Activate.ps1    # Windows PowerShell

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the development server
fastapi dev main.py
```

Open **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

## Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/courses` | Course list with filtering, sorting, pagination |
| GET | `/courses/{course_id}` | Single course or 404 |
| GET | `/stats` | Aggregate stats (bonus) |

## What was verified

All requests below were tested via `/docs` → *Try it out* and confirmed in the Response body.

| Request | Result |
|---------|--------|
| `GET /courses` | 6 courses; **ai-integration** first (32 likes), **api-design** last (11) |
| `GET /courses?is_elective=true` | 2 courses: ai-integration, api-design |
| `GET /courses?is_elective=false` | 4 courses: modern-frontend, web-security, backend-fastapi, databases-postgresql |
| `GET /courses?sort=title` | 6 courses alphabetically: ai-integration, api-design, backend-fastapi, modern-frontend, databases-postgresql, web-security |
| `GET /courses/web-security` | `200 OK` — Web Security Essentials |
| `GET /courses/nope` | `404` — `{"detail": "Course not found"}` |
| `GET /courses?page=1&page_size=2` | ai-integration, modern-frontend |
| `GET /courses?page=2&page_size=2` | web-security, backend-fastapi |
| `GET /courses?page=3&page_size=2` | databases-postgresql, api-design |
| `GET /courses?page=4&page_size=2` | `[]` |
| `GET /courses?page=0` | `422` — validation error (page must be ≥ 1) |
| `GET /courses?page_size=101` | `422` — validation error (page_size must be ≤ 100) |
| `GET /courses?q=react` | modern-frontend |
| `GET /courses?q=api` | api-design, backend-fastapi |
| `GET /stats` | `{"total": 6, "total_credits": 28, "electives": 2}` |

## Bonus features implemented

- `sort: Literal["popular", "title"]` — `/docs` shows a dropdown; `?sort=banana` returns 422.
- `page` and `page_size` validated with `Query(ge=1)` / `Query(ge=1, le=100)`.
- `q` — case-insensitive title search.
- `GET /stats` endpoint with a dedicated `Stats` Pydantic model.
