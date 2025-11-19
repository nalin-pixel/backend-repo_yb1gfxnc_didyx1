import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db
from schemas import Lead, Newsletter, Project, BlogPost, Testimonial

app = FastAPI(title="Energy4You API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Energy4You backend ready"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else ("✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set")
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["connection_status"] = "Connected"
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# Leads
@app.post("/leads")
def create_lead(payload: Lead):
    try:
        lead_id = create_document("lead", payload)
        return {"status": "ok", "id": lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Newsletter
@app.post("/newsletter")
def subscribe(payload: Newsletter):
    try:
        sub_id = create_document("newsletter", payload)
        return {"status": "ok", "id": sub_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Projects
@app.get("/projects", response_model=List[Project])
def list_projects(limit: Optional[int] = None):
    try:
        docs = get_documents("project", {}, limit)
        # Convert ObjectId and unknown fields gracefully
        sanitized = []
        for d in docs:
            d.pop("_id", None)
            sanitized.append(Project(**d))
        return sanitized
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/projects")
def add_project(payload: Project):
    try:
        proj_id = create_document("project", payload)
        return {"status": "ok", "id": proj_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Blog
@app.get("/blog", response_model=List[BlogPost])
def list_posts(limit: Optional[int] = None):
    try:
        docs = get_documents("blogpost", {}, limit)
        sanitized = []
        for d in docs:
            d.pop("_id", None)
            sanitized.append(BlogPost(**d))
        return sanitized
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/blog")
def add_post(payload: BlogPost):
    try:
        post_id = create_document("blogpost", payload)
        return {"status": "ok", "id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Testimonials
@app.get("/testimonials", response_model=List[Testimonial])
def list_testimonials(limit: Optional[int] = None):
    try:
        docs = get_documents("testimonial", {}, limit)
        sanitized = []
        for d in docs:
            d.pop("_id", None)
            sanitized.append(Testimonial(**d))
        return sanitized
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/testimonials")
def add_testimonial(payload: Testimonial):
    try:
        t_id = create_document("testimonial", payload)
        return {"status": "ok", "id": t_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Site Meta for SEO and CMS-like info
class SiteMeta(BaseModel):
    name: str
    tagline: str
    description: str
    language: str = "fr"


@app.get("/site-meta", response_model=SiteMeta)
def site_meta():
    return SiteMeta(
        name="Energy4You",
        tagline="Solutions d'énergie durable pour aujourd'hui et demain",
        description="Intégrateur français spécialisé en efficacité énergétique, photovoltaïque, stockage et optimisation pour particuliers et entreprises.",
        language="fr",
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
