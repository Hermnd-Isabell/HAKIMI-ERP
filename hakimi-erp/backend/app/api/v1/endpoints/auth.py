from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.api.deps import bearer_scheme, get_current_user
from app.core.database import get_db
from app.models.auth import User
from app.schemas.auth import TokenResponse, UserLogin, UserOut, UserRegister
from app.schemas.base import ResponseModel
from app.services.auth_service import auth_service


router = APIRouter()


@router.post("/register", response_model=ResponseModel[TokenResponse], status_code=status.HTTP_201_CREATED)
def register(
    *,
    db: Session = Depends(get_db),
    data: UserRegister,
):
    try:
        user = auth_service.create_user(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    session = auth_service.create_session(db, user, remember_me=False)
    return ResponseModel(
        data=TokenResponse(
            access_token=session.token,
            expires_at=session.expires_at,
            user=UserOut.model_validate(user),
        )
    )


@router.post("/login", response_model=ResponseModel[TokenResponse])
def login(
    *,
    db: Session = Depends(get_db),
    data: UserLogin,
):
    user = auth_service.authenticate(db, data.account, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect account or password")

    session = auth_service.create_session(db, user, remember_me=data.remember_me)
    return ResponseModel(
        data=TokenResponse(
            access_token=session.token,
            expires_at=session.expires_at,
            user=UserOut.model_validate(user),
        )
    )


@router.get("/me", response_model=ResponseModel[UserOut])
def me(current_user: User = Depends(get_current_user)):
    return ResponseModel(data=UserOut.model_validate(current_user))


@router.post("/logout", response_model=ResponseModel[bool])
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials and credentials.credentials:
        auth_service.revoke_session(db, credentials.credentials)
    return ResponseModel(data=True)
