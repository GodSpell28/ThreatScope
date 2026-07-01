from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.auth import User
from app.schemas.auth import UserCreate, UserLogin, TokenResponse, UserResponse, ROLES
from app.services.auth import (
    hash_password,
    verify_password,
    create_access_token,
    normalize_username,
    scopes_for_role,
    record_login,
)
from pydantic import EmailStr

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fake_current_user(x_token: str = "", db: Session = Depends(get_db)) -> User:
    if not x_token.startswith("token-"):
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Demo: token is not to token_id for readme demo simplicity.
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@router.post("/register", response_model=UserResponse)
async def register(payload: UserCreate, db: Session = Depends(get_db)):
    username = normalize_username(payload.username)
    if db.query(User).filter((User.username == username) | (User.email == payload.email)).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")
    user = User(
        username=username,
        email=str(payload.email).strip().lower(),
        hashed_password=hash_password(payload.password),
        role=str(payload.role),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: Session = Depends(get_db)):
    username = normalize_username(payload.username)
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is disabled")
    token = create_access_token(user)
    record_login(user)
    db.add(user)
    db.commit()
    return TokenResponse(access_token=token, role=user.role)


@router.get("/me", response_model=UserWithScopes)
async def me(current_user: User = Depends(fake_current_user)):
    return UserWithScopes(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
        scopes=scopes_for_role(current_user.role),
    )
