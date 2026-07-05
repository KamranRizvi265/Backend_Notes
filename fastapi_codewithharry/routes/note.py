from fastapi import APIRouter
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.note import Note
from config.db import db, collection
from schema.note import noteEntity, notesEntity

note = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")

@note.get("/")
async def read_root():
    return {"Hello": "World"}

# Item details
@note.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )
 
# Database test
@note.get("/db_test", response_class=HTMLResponse)
async def db_test(request: Request):
    result = list(collection.find({}, {"_id": 0, "title": 1, "description": 1, "important": 1}))
    return templates.TemplateResponse(
        request=request, name="db_test.html", context={"result": result}
    )

@note.post("/notes")
async def create_note(note: Note):
    collection.insert_one(dict(note))
    return noteEntity(collection.find_one({"title": note.title}))