from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from schema.post import PostSchema
from schema.user import UserCreate, UserRead, UserUpdate
from database.db import Post, create_db_and_tables, create_async_engine, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
import os
import shutil
import uuid
import tempfile
from app.users import fastapi_users, current_active_user, auth_backend

# Define the lifespan context manager to create the database and tables on startup
@asynccontextmanager
async def lifespan(app : FastAPI):
    await create_db_and_tables()
    yield 

app = FastAPI(lifespan=lifespan)

# Include the authentication router for JWT authentication
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

# Include the user management router for user-related operations
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

# Include the user management router for user-related operations
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)

# Include the user management router for user-related operations
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"]
)

# Include the user management router for user-related operations
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

@app.post("/upload")
async def upload_file(
    file : UploadFile = File(...),
    caption : str = Form(""),
    user : User = Depends(current_active_user),  # Get the currently authenticated user
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
                user_id = user.id,
                caption=caption,
                url = upload_result.url,
                file_type = "video" if (file.content_type or "").startswith("video") else "image",
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
    session : AsyncSession = Depends(get_async_session),
    user : User = Depends(current_active_user)  # Get the currently authenticated user
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    # Fetch the full user record from DB to ensure up-to-date info
    result_user = await session.execute(select(User))
    users = [row[0] for row in result_user.all()]
    user_dict = {u.id: u for u in users}

    posts_data = []
    for post in posts:
        posts_data.append(
            {
            "id" : str(post.id),
            "caption" : post.caption,
            "user_id" : str(post.user_id),
            "url" : post.url,
            "file_type" : post.file_type,
            "file_name" : post.file_name,
            "created_at" : post.created_at.isoformat(),
            "is_owner" : post.user_id == user.id,  # Check if the authenticated user is the owner of the post
            "email" : user_dict.get(post.user_id, {}).email if post.user_id in user_dict else None  # Include the email of the authenticated user
            }
        )

    if not posts_data:
        raise HTTPException(status_code=404, detail="No posts found")
    return {"post": posts_data}

@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_async_session),
    user : User = Depends(current_active_user)  # Get the currently authenticated user
):
    try:
        post_uuid = uuid.UUID(post_id)
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post : Post | None = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Check if the authenticated user is the owner of the post
        if str(post.user_id) != str(user.id):
            raise HTTPException(status_code=403, detail="You are not authorized to delete this post")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))