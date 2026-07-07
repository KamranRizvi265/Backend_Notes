from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from schema.post import PostSchema
from database.db import Post, create_db_and_tables, create_async_engine, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
import os
import shutil
import uuid
import tempfile

@asynccontextmanager
async def lifespan(app : FastAPI):
    await create_db_and_tables()
    yield 

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file : UploadFile = File(...),
    caption : str = Form(""),
    session : AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(file.filename or "")[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
            temp_file.seek(0)

        upload_result = imagekit.files.upload(
            file=open(temp_file_path, "rb"),
            file_name=file.filename or "",
            tags=["backend-upload"]
        )

        if upload_result and upload_result.file_id:
            post = Post(
                caption=caption,
                url = upload_result.url,
                file_type = "video" if file.content_type.startswith("video") else "image",
                file_name = upload_result.name
            )

            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as cleanup_error:
                print(f"Error cleaning up temporary file: {cleanup_error}")
        file.file.close()

@app.get("/feed")
async def get_feed(
    session : AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
            "id" : str(post.id),
            "caption" : post.caption,
            "url" : post.url,
            "file_type" : post.file_type,
            "file_name" : post.file_name,
            "created_at" : post.created_at.isoformat()
            }
        )

    return {"post": posts_data}