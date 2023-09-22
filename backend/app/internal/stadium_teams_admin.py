from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_admin, get_team, get_home_stadium, get_stadium, assign_home_stadium, remove_home_stadium, get_team_manager
from ..models import User, StadiumRead, TeamRead
from typing import List


##############################################  Stadium Teams Section  ############################################################################################################
stadium_teams_router = APIRouter(prefix="/stadium_teams",
                                 tags=["Stadium Teams"],
                                 dependencies=[Depends(oauth2_scheme)],
                                 responses={404: {"description": "Stadium team Not found"}},)


# get team home stadium
@stadium_teams_router.get("/get_team_home_stadium/{team_name}", response_model=StadiumRead)
async def get_team_home_stadium(team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    home_stadium = get_home_stadium(team_name)
    if not home_stadium:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} has no home stadium")
    return home_stadium


# get teams by home stadium
@stadium_teams_router.get("/get_teams_by_home_stadium/{stadium_name}", response_model=List[TeamRead])
async def get_teams_by_home_stadium(stadium_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if home stadium exists
    teams = get_stadium_home_teams(stadium_name)
    if not teams:
        raise HTTPException(
            status_code=404, detail=f"Stadium with name: {stadium_name} not found")
    return teams


# get stadium home teams
@stadium_teams_router.get("/get_stadium_home_teams/{stadium_name}", response_model=List[TeamRead])
async def get_stadium_home_teams(stadium_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return get_stadium_home_teams(stadium_name)


# remove team home stadium
@stadium_teams_router.delete("/remove_team_home_stadium/{team_name}")
async def remove_team_home_stadium(team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    # remove team home stadium
    return remove_home_stadium(team)


# assign team home stadium
@stadium_teams_router.put("/assign_team_home_stadium/{team_name}/{stadium_name}", response_model=TeamRead)
async def assign_team_home_stadium(team_name: str, stadium_id: int, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    # check if stadium exist
    stadium = get_stadium(stadium_id)
    if not stadium:
        raise HTTPException(
            status_code=404, detail=f"Stadium with stadium ID: {stadium_id} not found")
    # check if home stadium is already assigned to the team
    home_stadium = get_home_stadium(team_name)
    if home_stadium and home_stadium.stadium_id == stadium.stadium_id:
        raise HTTPException(
            status_code=404, detail=f"Stadium with stadium ID: {stadium_id} is already assigned to team {team_name}")
    # assign home stadium to team
    return assign_home_stadium(team, stadium)
