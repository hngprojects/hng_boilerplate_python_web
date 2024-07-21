from api.v1.models.user import User, WaitlistUser
from api.v1.models.org import Organization
from api.v1.models.profile import Profile
from api.v1.models.product import Product
from api.v1.models.subscription import Subscription
from api.v1.models.blog import Blog
from api.v1.models.job import Job
from api.v1.models.invitation import Invitation
from api.v1.models.role import Role
from api.v1.models.permission import Permission
from api.v1.models.newsletter import NEWSLETTER
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class PermissionBase(BaseModel):
    name: str
    description: Optional[str]

class PermissionCreate(PermissionBase):
    description: str

class PermissionUpdate(PermissionBase):
    description: Optional[str] = None

class Permission(PermissionBase):
    id: UUID
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
