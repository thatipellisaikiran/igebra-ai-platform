from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import LoginRequest, TokenResponse, UserResponse, DemoAccountInfo
from app.core.security import verify_credentials, create_access_token, DEMO_USERS

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(creds: LoginRequest):
    user = verify_credentials(creds.email, creds.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Use one of the pre-seeded demo accounts."
        )
    token = create_access_token(data={"sub": user["id"], "role": user["role"]})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(**user)
    )

@router.get("/demo-accounts", response_model=List[DemoAccountInfo])
def get_demo_accounts():
    accounts = []
    for email, u in DEMO_USERS.items():
        accounts.append(
            DemoAccountInfo(
                id=u["id"],
                email=u["email"],
                role=u["role"],
                label=f"{u['full_name']} ({u['role'].capitalize()})",
                password=u["password"],
                description=u.get("grade") or u.get("department", "Demo User")
            )
        )
    return accounts

