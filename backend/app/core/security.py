from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

from app.core.config import settings

# Pre-seeded Hackathon Demo Accounts
DEMO_USERS = {
    "student@gapfinder.ai": {
        "id": "usr_std_001",
        "email": "student@gapfinder.ai",
        "full_name": "Aarav Sharma",
        "role": "student",
        "password": "student123",
        "grade": "Class 12 - Pre-Med / CBSE",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Aarav"
    },
    "teacher@gapfinder.ai": {
        "id": "usr_tch_001",
        "email": "teacher@gapfinder.ai",
        "full_name": "Dr. Meenakshi Sundaram",
        "role": "teacher",
        "password": "teacher123",
        "department": "Department of Biological Sciences",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Meenakshi"
    }
}

def verify_credentials(email: str, password: str) -> Optional[dict]:
    user = DEMO_USERS.get(email.strip().lower())
    if user and user["password"] == password:
        user_copy = dict(user)
        user_copy.pop("password", None)
        return user_copy
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

