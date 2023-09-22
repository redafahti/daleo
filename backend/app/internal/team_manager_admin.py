from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_user, get_current_active_admin, get_teams_managers, get_team, get_team_manager, get_manager, get_manager_teams, assign_team_manager, remove_team_manager, update_manager
from ..models import User, ManagerRead, TeamRead, ManagerUpdate
from typing import List


############################# Team Manager Admin Section ###########################################################################################################
team_manager_router = APIRouter(
    prefix="/team_manager",
    tags=["Team Manager"],
    dependencies=[Depends(oauth2_scheme)],
    responses={418: {"description": "I'm an Administrator"}},)


# get all teams managers
@team_manager_router.get("/get_teams_managers", response_model=List[ManagerRead])
async def get_all_team_managers(current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return get_teams_managers()


# get team manager
@team_manager_router.get("/get_team_manager/{team_name}", response_model=ManagerRead)
async def read_team_manager(team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    manager = get_team_manager(team)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} has no manager")
    return manager


# get manager teams
@team_manager_router.get("/get_manager_teams/{manager_username}", response_model=List[TeamRead])
async def read_manager_teams(manager_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    manager = get_manager(manager_username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {manager_username} not found")
    teams = get_manager_teams(manager)
    if not teams:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {manager_username} has no teams")
    return teams


# assign team manager
@team_manager_router.put("/assign_team_manager/{team_name}/{username}", response_model=TeamRead)
async def assign_new_team_manager(team_name: str, username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if user exists
    user_db = get_user(username)
    if not user_db:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if manager exists
    manager = get_manager(username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {username} not found")
    # check if user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id == user_db.id:
        raise HTTPException(
            status_code=404, detail=f"{user_db.username} is already the manager of: {team_name}")
    # assign new manager to team
    return assign_team_manager(team, manager)


# remove team manager
@team_manager_router.put("/remove_team_manager/{team_name}", response_model=TeamRead)
async def remove_manager_from_team(team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if team has a manager
    manager = get_team_manager(team)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} has no manager")
    # remove team manager
    return remove_team_manager(team)


# team manager rating
@team_manager_router.put("/manager_rating/{team_name}/{manager_rating}", response_model=ManagerRead)
async def manager_rating(team_name: str, manager_rating: int, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} not found")
    # get team manager
    manager = get_team_manager(team)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Team {team_name} has no manager")
    # Check if the manager_rating is between 0 and 5
    if manager_rating < 0 or manager_rating > 5:
        raise HTTPException(
            status_code=400, detail="Manager rating must be between 0 and 5"
        )
    # Calculate the average rating and update the rating count
    manager_rating_count = manager.manager_rating_count + 1
    manager_rating_total = manager.manager_rating * manager.manager_rating_count
    manager_rating_total += manager_rating
    manager_rating_average = manager_rating_total / manager_rating_count
    manager_rating_average = round(manager_rating_average, 2)

    # Update manager
    manager_update = ManagerUpdate(
        username=manager.username,
        manager_rating=manager_rating_average,
        manager_rating_count=manager_rating_count
    )
    return update_manager(manager_update)
