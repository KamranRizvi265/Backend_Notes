from fastapi import FastAPI, HTTPException
from schema.post import Posts

app = FastAPI()

text_posts = {1 : {"title":"New Post", "content":"cool test post"},
    2 : {"title":"Tech Update", "content":"software patch released"},
    3 : {"title":"Morning Routine", "content":"coffee and meditation"},
    4 : {"title":"Book Review", "content":"highly recommend this"},
    5 : {"title":"Travel Vlog", "content":"exploring hidden caves"},
    6 : {"title":"Daily Quote", "content":"keep moving forward"},
    7 : {"title":"Fitness Goal", "content":"completed five miles"},
    8 : {"title":"Recipe Share", "content":"easy vegan lasagna"},
    9 : {"title":"Movie Night", "content":"watching classic sci-fi"},
    10 : {"title":"Coding Tip", "content":"always comment code"}
}

@app.get("/posts")
def get_all_posts(limit : int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id : int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post : Posts):
    post = {"title": post.title,"description": post.description}
    text_posts[max(text_posts.keys())+1] = post
    return post