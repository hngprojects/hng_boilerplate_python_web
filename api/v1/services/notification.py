from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.core.base.services import Service
from api.db.database import get_db
from api.v1.models.notifications import Notification
from api.v1.models.user import User
from api.utils.email_service import send_mail
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from api.v1.schemas.notification import NotificationCreate

# from api.v1.schemas.notification import NotificationRead



class NotificationService(Service):
    
    def create_notification(
        self,
        notification: NotificationCreate,
        user: User,
        db: Session = Depends(get_db),
    ):
        new_notification = Notification(
            user_id=user.id,
            title=notification.title,
            message=notification.message,
        )
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)
        return new_notification
    
    
    
    
    def mark_notification_as_read(
        self,
        notification_id: str,
        user: User,
        db: Session = Depends(get_db),
    ):
        notification = (
            db.query(Notification)
            .filter(Notification.id == notification_id, Notification.user_id == user.id)
            .first()
        )

        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        # check if the notification is marked as read
        if notification.status == "read":
            return

        # update notification status
        notification.status = "read"

        # commit changes
        db.commit()
        


    def delete(
        self,
        notification_id: str,
        user: User,
        db: Session = Depends(get_db),
    ):
        notification = (
            db.query(Notification).filter(Notification.id == notification_id).first()
        )

        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        if notification.user_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to delete this notification",
            )

        db.delete(notification)
        db.commit()
        db.refresh()

    def get_current_user_notifications(self, user: User, db: Session = Depends(get_db)):
        '''Endpoint to get current user notifications'''
        
        return {"notifications": user.notifications}
    
    # def fetch(
    #     self,
    #     notification_id: str,
    #     user: User,
    #     db: Session = Depends(get_db),
    # ):
    #     notification = (
    #         db.query(Notification)
    #         .filter(Notification.id == notification_id)
    #         .first()
    #     )

    #     if not notification:
    #         raise HTTPException(status_code=404, detail="Notification not found")

    #     if notification.user_id != user.id:
    #         print(f"Permission check failed. User ID: {user.id}, Notification User ID: {notification.user_id}")
    #         raise HTTPException(status_code=403, detail="You do not have permission to view this notification")

    #     return notification

    def create(self):
        super().create()

    def fetch(self, db: Session):
        super().fetch()

    def fetch_all(self):
        super().fetch_all()

    def update(self):
        super().update()


notification_service = NotificationService()
