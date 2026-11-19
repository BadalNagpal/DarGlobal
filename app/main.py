import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

from app.search_engine import RealEstateSearchEngine
from app.openrouter_client import OpenRouterClient

load_dotenv()

app = FastAPI(title="DarGlobal & Wasalt Real Estate AI Chatbot")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize Search Engine & OpenRouter Client
search_engine = RealEstateSearchEngine()
openrouter_client = OpenRouterClient()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    openrouter_api_key: Optional[str] = None
    model: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    stats = {
        "darglobal_count": len(search_engine.darglobal_projects),
        "wasalt_count": len(search_engine.wasalt_properties),
        "total_count": len(search_engine.darglobal_projects) + len(search_engine.wasalt_properties),
        "has_api_key": openrouter_client.is_configured
    }
    return templates.TemplateResponse(request, "index.html", context={"stats": stats})

@app.get("/api/properties")
async def get_properties(q: Optional[str] = ""):
    results = search_engine.search(q, limit=10)
    return results

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    if not req.messages:
        return JSONResponse(status_code=400, content={"error": "No messages provided"})
    
    last_user_message = req.messages[-1].content
    search_results = search_engine.search(last_user_message, limit=5)
    
    # Configure dynamic key if provided by user in UI
    client = openrouter_client
    if req.openrouter_api_key:
        client = OpenRouterClient(api_key=req.openrouter_api_key, model=req.model)
        
    response_text = ""
    engine_used = "OpenRouter AI"
    
    if client.is_configured:
        # Build context from scraped search results
        context_str = json_context_summary(search_results)
        msgs = [{"role": m.role, "content": m.content} for m in req.messages]
        response_text = client.generate_chat_response(msgs, context_str)
        
    if not response_text:
        # Intelligent fallback to RAG Expert Engine using scraped real estate DB
        engine_used = "RealEstate Knowledge Advisor (Scraped DB)"
        response_text = search_engine.generate_expert_response(last_user_message, search_results)
        
    return {
        "reply": response_text,
        "engine": engine_used,
        "search_results": search_results
    }

def json_context_summary(results: dict) -> str:
    parts = []
    if results.get("darglobal"):
        parts.append("DarGlobal Luxury Projects:")
        for p in results["darglobal"]:
            parts.append(
                f"- Project: {p.get('project_name')}, Location: {p.get('location')}, Type: {p.get('project_type')}, "
                f"Partners: {', '.join(p.get('brand_partners', []))}, Starting Price: {p.get('starting_price')}, "
                f"Highlights: {p.get('description')}, URL: {p.get('url')}"
            )
    if results.get("wasalt"):
        parts.append("\nWasalt Saudi Real Estate Properties:")
        for p in results["wasalt"]:
            loc = p.get('location', {})
            specs = p.get('specs', {})
            parts.append(
                f"- Property: {p.get('title')}, City: {loc.get('city')}, District: {loc.get('district')}, "
                f"Price: {p.get('price')} SAR, Type: {p.get('property_type')}, Category: {p.get('category')}, "
                f"Specs: {specs.get('bedrooms')} Beds, {specs.get('bathrooms')} Baths, {specs.get('area_sqm')} SQM, URL: {p.get('url')}"
            )
    return "\n".join(parts)
