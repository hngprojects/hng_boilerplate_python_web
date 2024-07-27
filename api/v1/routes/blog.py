from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.v1.models.blog import Blog
from api.v1.schemas.blog import BlogResponse
from api.db.database import get_db
from api.v1.routes.user import get_current_user_details
from api.v1.services.blog import BlogService

blog = APIRouter(prefix="/blogs", tags=["Blog"])


@blog.get("/", response_model=List[BlogResponse])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).filter(Blog.is_deleted == False).all()
    if not blogs:
        return []
    return blogs


@blog.post("/{blog_id}/like")
async def like_blog(blog_id: UUID, request: Request, db: Session = Depends(get_db),
                    current_user=Depends(get_current_user_details)):
    """
    Endpoint to allow users to like a blog post.
    """
    blog_service = BlogService(db)
    return await blog_service.like_blog_service(blog_id, request, current_user)
