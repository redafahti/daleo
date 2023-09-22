from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_user, get_current_active_superuser, update_user
from ..models import User, UserUpdate

############################# Admin Section ############################################################################################################
superuser_router = APIRouter(
    prefix="/superuser",
    tags=["Superuser"],
    dependencies=[Depends(oauth2_scheme)],
    responses={418: {"description": "I'm a Superuser"}},)


# Admin root
@superuser_router.post("/", response_model=dict)
async def read_root(current_superuser: User = Security(get_current_active_superuser, scopes=["superuser"])):
    return {"message": "Welcome to the Team Up Admin section "}


# system status
@superuser_router.get("/status", response_model=dict)
async def get_status(current_superuser: User = Security(get_current_active_superuser, scopes=["superuser"])):
    return {"message": "Status OK"}


# make user superuser
@superuser_router.patch("/make_superuser/{username}")
async def make_superuser(username: str, current_superuser: User = Security(get_current_active_superuser, scopes=["superuser"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    update_user(user, UserUpdate(is_superuser=True))
    return {"message": f"User with username {username} is superuser now"}


# make user admin
@superuser_router.patch("/make_admin/{username}")
async def make_admin(username: str, current_superuser: User = Security(get_current_active_superuser, scopes=["superuser"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    update_user(user, UserUpdate(is_admin=True))
    return {"message": f"User with username {username} is admin now"}


# remove user superuser
@superuser_router.patch("/remove_superuser/{username}")
async def remove_superuser(username: str, current_superuser: User = Security(get_current_active_superuser, scopes=["superuser"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    update_user(user, UserUpdate(is_superuser=False))
    return {"message": f"User with username {username} is not superuser now"}


# remove user admin
@superuser_router.patch("/remove_admin/{username}")
async def remove_admin(username: str, current_superuser: User = Security(get_current_active_superuser, scopes=["superuser"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    update_user(user, UserUpdate(is_admin=False))
    return {"message": f"User with username {username} is not admin now"}
