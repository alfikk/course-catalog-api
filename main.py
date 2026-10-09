from typing import Annotated, List, Literal, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel

from data import find_course, get_all_courses
from models import Course

app = FastAPI(title="Course Catalog API")


# ---------------------------------------------------------------------------
# Pagination dependency
# ---------------------------------------------------------------------------

def pagination(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict:
    """Return offset and limit derived from page / page_size."""
    return {"offset": (page - 1) * page_size, "limit": page_size}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Course Catalog API is running"}


@app.get("/courses", response_model=List[Course])
def list_courses(
    is_elective: Optional[bool] = None,
    sort: Literal["popular", "title"] = "popular",
    q: Optional[str] = None,
    p: dict = Depends(pagination),
):
    courses = get_all_courses()

    # Filter by elective flag (use `is not None` to correctly handle False)
    if is_elective is not None:
        courses = [c for c in courses if c.is_elective == is_elective]

    # Optional search by title substring (bonus)
    if q is not None:
        courses = [c for c in courses if q.lower() in c.title.lower()]

    # Sorting
    if sort == "title":
        courses = sorted(courses, key=lambda c: c.title)
    else:  # "popular" — by likes descending
        courses = sorted(courses, key=lambda c: c.likes, reverse=True)

    # Pagination — filter & sort first, then slice
    offset = p["offset"]
    limit = p["limit"]
    courses = courses[offset: offset + limit]

    return courses


@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: str):
    course = find_course(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# ---------------------------------------------------------------------------
# Bonus: GET /stats
# ---------------------------------------------------------------------------

class Stats(BaseModel):
    total: int
    total_credits: int
    electives: int


@app.get("/stats", response_model=Stats)
def get_stats():
    all_courses = get_all_courses()
    return Stats(
        total=len(all_courses),
        total_credits=sum(c.credits for c in all_courses),
        electives=sum(1 for c in all_courses if c.is_elective),
    )
