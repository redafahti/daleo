from fastapi import APIRouter, Depends, HTTPException, Security
from ..dependencies import oauth2_scheme, get_current_active_user, get_team, get_team_rating, get_team, get_stadium, get_stadium_home_teams, get_teams_by_rating
from ..models import User, TeamRead
from typing import List


################################################# Teams Main Section  ############################################################################################################
teams_router = APIRouter(prefix="/teams",
                         tags=["Teams"],
                         dependencies=[Depends(oauth2_scheme)],
                         responses={404: {"description": "Team Not found"}},)


# teams root
@teams_router.get("/")
async def read_root(current_user: User = Security(get_current_active_user, scopes=["teams"])):
    return{"Welcome to Team Up Teams Section"}


# get team
@teams_router.get("/get_team/{team_name}", response_model=TeamRead)
async def read_team(team_name: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    return team


# get team rating
@teams_router.get("/get_team_rating/{team_name}", response_model=int)
async def read_team_rating(team_name: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} not found")
    return get_team_rating(team)


# find teams by home stadium
@teams_router.get("/find_teams_by_stadium/{stadium_id}", response_model=List[TeamRead])
async def find_teams_by_stadium(stadium_id: int):
    # check if stadium exists
    stadium = get_stadium(stadium_id)
    if not stadium:
        raise HTTPException(
            status_code=404, detail=f"Stadium with id: {stadium_id} not found")
    teams = get_stadium_home_teams(stadium)
    if not teams:
        raise HTTPException(
            status_code=404, detail=f"No teams found in stadium with id: {stadium_id}")
    return teams


# find teams by rating
@teams_router.get("/find_teams_by_rating/{rating}", response_model=List[TeamRead])
async def find_teams_by_rating(rating: float):
    teams = get_teams_by_rating(rating)
    if not teams:
        raise HTTPException(
            status_code=404, detail=f"No teams found with rating: {rating}")
    return teams
