import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.auth import User, UserSession
from app.schemas.auth import UserRegister


PBKDF2_ITERATIONS = 200_000


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
        return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"

    @staticmethod
    def verify_password(password: str, encoded: str) -> bool:
        try:
            algorithm, iterations, salt_hex, hash_hex = encoded.split("$")
            if algorithm != "pbkdf2_sha256":
                return False
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(hash_hex)
            actual = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                int(iterations),
            )
            return hmac.compare_digest(actual, expected)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def get_user_by_identity(db: Session, identity: str) -> Optional[User]:
        identity = identity.strip().lower()
        return db.query(User).filter(
            or_(func.lower(User.username) == identity, User.email == identity)
        ).first()

    @staticmethod
    def create_user(db: Session, data: UserRegister) -> User:
        username = data.username.strip()
        email = data.email.strip().lower()

        if db.query(User).filter(func.lower(User.username) == username.lower()).first():
            raise ValueError("Username already exists")
        if db.query(User).filter(User.email == email).first():
            raise ValueError("Email already exists")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("A valid email address is required")

        user = User(
            username=username,
            email=email,
            password_hash=AuthService.hash_password(data.password),
            full_name=data.full_name.strip() if data.full_name and data.full_name.strip() else None,
            role="USER",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, account: str, password: str) -> Optional[User]:
        user = AuthService.get_user_by_identity(db, account)
        if not user or not user.is_active:
            return None
        if not AuthService.verify_password(password, user.password_hash):
            return None
        user.last_login_time = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_session(db: Session, user: User, remember_me: bool) -> UserSession:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=30 if remember_me else 1)
        session = UserSession(user_id=user.id, token=token, expires_at=expires_at)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_user_by_token(db: Session, token: str) -> Optional[User]:
        session = db.query(UserSession).filter(
            UserSession.token == token,
            UserSession.expires_at > datetime.utcnow(),
        ).first()
        if not session:
            return None
        return db.query(User).filter(User.id == session.user_id, User.is_active.is_(True)).first()

    @staticmethod
    def revoke_session(db: Session, token: str) -> None:
        db.query(UserSession).filter(UserSession.token == token).delete()
        db.commit()


auth_service = AuthService()
