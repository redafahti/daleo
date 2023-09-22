from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_user, get_current_active_admin, all_managers, create_manager, get_manager, update_manager, get_manager_teams, assign_team_manager, delete_manager
from ..models import User, ManagerRead, ManagerCreate, ManagerUpdate
from typing import List


########################### Managers Admin Section ############################################################################################################
managers_admin_router = APIRouter(
    prefix="/managers_admin",
    tags=["Managers Admin"],
    dependencies=[Depends(oauth2_scheme)],
    responses={418: {"description": "I'm an Administrator"}},)


# get all managers
@managers_admin_router.get("/get_managers", response_model=List[ManagerRead])
async def get_all_managers(current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return all_managers()


# create manager
@managers_admin_router.post("/create_manager/{username}", response_model=ManagerRead)
async def create_new_manager(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if user exists
    user_db = get_user(username)
    if not user_db:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    # check if user is already a manager
    if user_db.manager_id:
        raise HTTPException(
            status_code=404, detail=f"User with username: {username} already has a manager profile")
    # check if user has all the required fields
    new_manager = ManagerCreate(
        username=username, user_id=user_db.id, manager_rating=0, manager_rating_count=0)
    return create_manager(new_manager)


# get manager
@managers_admin_router.get("/get_manager/{username}", response_model=ManagerRead)
async def get_manager_profile(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    manager = get_manager(username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {username} not found")
    return manager


# update manager
@managers_admin_router.put("/update_manager/{username}", response_model=ManagerRead)
async def update_manager_profile(manager_username: str, season_rate: int | None = None, current_admin: User = Security(get_current_active_admin, scopes=["managers"])):
    # check if user is a manager
    manager = get_manager(manager_username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"User: {manager_username} has no manager profile")
    # check if manager fields are valid
    manager_update = ManagerUpdate(
        username=manager_username, manager_season_rate=season_rate)
    return update_manager(manager_update)


# delete manager
@managers_admin_router.delete("/delete_manager/{username}")
async def delete_manager_profile(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    manager = get_manager(username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {username} not found")
    # check if current admin is a manager and create a new manager if not
    admin_manager = get_manager(current_admin.username)
    if not admin_manager:
        new_manager = ManagerCreate(
            username=current_admin.username, user_id=current_admin.id, manager_rating=0, manager_rating_count=0)
        admin_manager = create_manager(new_manager)
    # check if manager has teams and make admin_manager a team manager if so
    teams = get_manager_teams(manager)
    if teams:
        for team in teams:
            assign_team_manager(team, admin_manager)
    return delete_manager(manager)
