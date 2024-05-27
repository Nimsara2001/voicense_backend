from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from controller.auth_controller import authenticate_user, create_access_token, create_refresh_token, create_user, get_current_user, home_screens, frontend_urls
from model.user import SignupRequest, User


router = APIRouter(
    prefix="/auth",
)

# @router.post("/signup")
# async def signup():
#     return await {"message": "Signup page"}

# @router.post("/login")
# async def login():
#     return {"message": "Login page"}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/signup")
async def signup(signup_request: SignupRequest):
    return await create_user(
        signup_request.username,
        signup_request.password,
        signup_request.first_name,
        signup_request.last_name,
        signup_request.user_type
    )   


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):

    user_type = current_user.user_type

    if user_type not in home_screens:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user type",
        )

    home_screen = home_screens[user_type]
    frontend_url = frontend_urls[user_type]
    return {"home_screen": home_screen, "frontend_url": frontend_url, "user": current_user}

@router.post("/refresh-token")
async def refresh_token(current_user: User = Depends(get_current_user)):
    access_token = create_access_token(
        data={"sub": current_user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# hansaka branch
