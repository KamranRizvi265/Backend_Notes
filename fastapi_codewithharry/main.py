# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pymongo import MongoClient

# app = FastAPI()

# # Static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Templates
# templates = Jinja2Templates(directory="templates")

# # Database connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client["firstdb"]
# collection = db["firstcollection"]

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# # Item details
# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"id": id}
#     )
 
# # Database test
# @app.get("/db_test", response_class=HTMLResponse)
# async def db_test(request: Request):
#     result = list(collection.find({}, {"_id": 0, "name": 1, "message": 1}))
#     return templates.TemplateResponse(
#         request=request, name="db_test.html", context={"result": result}
#     )