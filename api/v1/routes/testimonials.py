from fastapi import(
    HTTPException,
    APIRouter,
    Request,
    Depends,
    status
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.v1.models.testimonials import Testimonial
from api.v1.schemas.testimonial import (
    UpdateTestimonial, 
    TestimonialCreate, 
    TestimonialResponse, 
    SuccessResponse,
 UpdateTestimonialResponse, 
BaseTestimonialResponse

)
from api.db.database import get_db, Base, engine
from typing import Annotated
from api.utils.dependencies import get_current_user


Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session , Depends(get_db)]

router = APIRouter(prefix="/api/v1", tags=["testimonials"])

class CustomException(HTTPException):
    """
    Custom error handling
    """
    def __init__(self, status_code: int, detail: dict):
        super().__init__(status_code=status_code, detail=detail)
        self.message = detail.get("message")
        self.success = detail.get("success")
        self.status_code = detail.get("status_code")

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "success": exc.success,
            "status_code": exc.status_code
        }
    )


@router.post('/testimonials', response_model = SuccessResponse)
def create_testimonial(testimonial: TestimonialCreate, db: db_dependency, current_user: dict = Depends(get_current_user)):
    db_testimonial = Testimonial(
        firstname=testimonial.firstname,
        lastname=testimonial.lastname,
        content=testimonial.content,
        user_id=current_user.id
    )
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    
    response_data = TestimonialResponse(
        id=db_testimonial.id,
        firstname=db_testimonial.firstname,
        lastname=db_testimonial.lastname,
        content=db_testimonial.content,
        created_at=db_testimonial.created_at,
        updated_at=db_testimonial.updated_at
    )
    
    return SuccessResponse(
        status="success",
        message="Testimonial created successfully",
        data=response_data
    )

@router.put('/testimonials/{testimonial_id}', response_model=UpdateTestimonialResponse)
def update_testimonial(testimonial_id : str, request : UpdateTestimonial , db : db_dependency ):
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()

    if not testimonial:
        raise CustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=   {
                    "status": "Bad Request",
                    "message": "Client error",
                     "status_code": 400
                     }
                    )
    testimonial.content = request.content
    db.commit()
    
    response_text = BaseTestimonialResponse(
        user_id=testimonial.user_id,
        content=testimonial.content,
        updated_at= testimonial.updated_at

    )
    return UpdateTestimonialResponse(
        status=status.HTTP_200_OK,
        message='Testimonial Updated Successfully',
        data= response_text
    )
    
    
 


