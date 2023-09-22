from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_admin, all_teams, get_team, update_team, delete_team, update_team_rating
from ..models import User, TeamRead, TeamUpdate
from typing import List

############################################## Team Admin Section ###############################################################################################
teams_admin_router = APIRouter(
    prefix="/teams_admin",
    tags=["Teams Admin"],
    dependencies=[Depends(oauth2_scheme)],
    responses={418: {"description": "I'm an Administrator"}},)


# get all teams
@teams_admin_router.get("/get_teams", response_model=List[TeamRead])
async def get_all_teams(current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return all_teams()


# get team
@teams_admin_router.get("/get_team/{team_name}", response_model=TeamRead)
async def read_team(team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    return team


# update team
@teams_admin_router.put("/update_team/{team_name}", response_model=TeamRead)
async def team_update(team_name: str, team_logo: str | None = None, team_home_color_jersey: str | None = None, team_away_color_jersey: str | None = None, team_home_color_shorts: str | None = None, team_away_color_shorts: str | None = None, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    # check if team has all the required fields
    team_update = TeamUpdate(team_name=team_name, team_logo=team_logo, team_home_color_jersey=team_home_color_jersey, team_away_color_jersey=team_away_color_jersey,
                             team_home_color_shorts=team_home_color_shorts, team_away_color_shorts=team_away_color_shorts)
    return update_team(team_update)


# update team rating
@teams_admin_router.put("/update_team_rating/{team_name}", response_model=TeamRead)
async def team_rating_update(team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} not found")
    return update_team_rating(team)


# delete team
@teams_admin_router.delete("/delete_team/{team_name}")
async def team_delete(team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    return delete_team(team_name)
