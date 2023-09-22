from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_user, get_matches, get_match, get_stadium, get_stadium_home_teams, get_team, update_match, delete_match
from ..models import User, MatchRead
from typing import List
from datetime import datetime, timedelta


####################################### Matches Admin Section ######################################################################################
matches_admin_router = APIRouter(prefix="/matches_admin",
                                 tags=["Matches Admin"],
                                 dependencies=[Depends(oauth2_scheme)],
                                 responses={404: {"description": "Match Not found"}},)


# get all matches
@matches_admin_router.get("/get_matches", response_model=List[MatchRead])
async def all_matches(current_user: User = Security(get_current_active_user, scopes=["matches"])):
    return get_matches()


# get match
@matches_admin_router.get("/get_match/{match_id}", response_model=MatchRead)
async def read_match(match_id: int, current_user: User = Security(get_current_active_user, scopes=["matches"])):
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with id {match_id} not found")
    return match


# update match
@matches_admin_router.put("/update_match/{match_id}")
async def match_update(match_id: int, home_team_name: str | None = None, away_team_name: str | None = None, match_duration: int | None = None, match_start_time: datetime | None = None, match_end_time: datetime | None = None, stadium_name: str | None = None, match_status: str | None = None, match_type: str | None = None, match_prize: int | None = None, current_user: User = Security(get_current_active_user, scopes=["matches"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"match with match id {match_id} not found")
    # check if stadium exists
    if stadium_name:
        stadium = get_stadium(stadium_name)
        if not stadium:
            raise HTTPException(
                status_code=404, detail=f"stadium with stadium name {stadium_name} not found")
        match.stadium_id = stadium.stadium_id
    # check if home team is in the stadium home teams
    if home_team_name:
        home_teams = get_stadium_home_teams(stadium_name)
        if home_team_name not in home_teams:
            raise HTTPException(
                status_code=404, detail=f"home team with team name {home_team_name} not found in stadium {stadium_name}")
        match.home_team_id = home_team_name
    # check if away team are valid
    if away_team_name:
        away_team = get_team(away_team_name)
        if not away_team:
            raise HTTPException(
                status_code=404, detail=f"away team with team name {away_team_name} not found")
        match.away_team_id = away_team_name
    # check if match start time is valid
    if match_start_time:
        if match_start_time < datetime.now():
            raise HTTPException(
                status_code=404, detail=f"match start time {match_start_time} is not valid")
        match.match_start_time = match_start_time
    # check if match end time is valid
    if match_end_time:
        if match_end_time < match_start_time:
            raise HTTPException(
                status_code=404, detail=f"match end time {match_end_time} is before match start time {match_start_time}")
        match.match_end_time = match_end_time
    # update match
    match = update_match(match_id=match_id, home_team_name=home_team_name, away_team_name=away_team_name, match_duration=match_duration, match_start_time=match_start_time,
                         match_end_time=match_end_time, stadium_name=stadium_name, match_status=match_status, match_type=match_type, match_prize=match_prize)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"match with match id {match_id} not updated")
    return match


# delete match
@matches_admin_router.delete("/delete_match/{match_id}")
async def match_delete(match_id: int, current_user: User = Security(get_current_active_user, scopes=["matches"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"match with match id {match_id} not found")
    # delete match
    delete_match(match_id)
    return {"message": f"match with match id {match_id} deleted successfully"}
