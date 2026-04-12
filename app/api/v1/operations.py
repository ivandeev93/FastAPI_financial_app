from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import OperationRequest

from app.service import operations as operations_service
from app.dependency import get_db, get_current_user
from app.models import User


router = APIRouter()

@router.post("/operations/income")
def add_income(operation: OperationRequest, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return operations_service.add_income(db, current_user, operation)


@router.post("/operations/expense")
def add_expense(operation: OperationRequest, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return operations_service.add_expense(db, current_user, operation)