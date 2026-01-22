import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .deps import get_current_user
from ..core.config import settings
from ..core.database import get_db
from ..core.redis_utils import set_linking_token
from ..core.security import get_password_hash, verify_password, create_access_token
from ..models.transaction import TariffType
from ..models.user import User
from ..schemas.auth import Token, Login
from ..schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )

    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        password_hash=hashed_password,
        name=user_in.name,
        tariff=TariffType.FREE
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_user.transaction_count = 0
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: Login, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == form_data.email).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/linking-token")
def get_linking_token(current_user: User = Depends(get_current_user)):

    token = str(uuid.uuid4())

    set_linking_token(token, current_user.id)

    return {"token": token, "instructions": f"Send this token to the bot: {token}"}
