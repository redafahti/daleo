from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_user, get_referee, get_referee_matches, get_match, get_team, get_team_manager, assign_match_referee, remove_match_referee
from ..models import User, MatchRead
from typing import List


##################### Match Referees Section ############################################################################################################
match_referee_router = APIRouter(prefix="/match_referee",
                                 tags=["Match Referee"],
                                 dependencies=[Depends(oauth2_scheme)],
                                 responses={404: {"description": "Match referee Not found"}},)


# get referee matches
@match_referee_router.get("/get_referee_matches/{username}", response_model=List[MatchRead])
async def read_referee_matches(username: str, current_user: User = Security(get_current_active_user, scopes=["referees"])):
    referee = get_referee(username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username {username} not found")
    matches = get_referee_matches(referee.referee_id)
    if not matches:
        raise HTTPException(
            status_code=404, detail=f"Referee with username {username} has no matches")
    return matches


# Add referee to match
@match_referee_router.post("/add_referee_to_match/{match_id}/{username}")
async def add_referee_to_match(match_id: int, username: str, current_user: User = Security(get_current_active_user, scopes=["matches"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with id: {match_id} not found")
    # check if referee exists
    referee = get_referee(username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username: {username} not found")
    # get match home team manager
    home_team = match.home_team_name
    team = get_team(home_team)
    team_manager = get_team_manager(team)
    # check if current user is the home team manager
    if current_user.id != team_manager.user_id:
        raise HTTPException(
            status_code=404, detail=f"Current user is not the home team manager")
    # assign referee to match
    return assign_match_referee(match)


# Remove referee from match
@match_referee_router.put("/remove_referee_from_match/{match_id}/{username}")
async def remove_referee_from_match(match_id: int, referee_username: str, current_user: User = Security(get_current_active_user, scopes=["matches"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with id: {match_id} not found")
    # check if referee exists
    referee = get_referee(referee_username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username: {referee_username} not found")
    # get match home team manager
    home_team = match.home_team_name
    team = get_team(home_team)
    team_manager = get_team_manager(team)
    # check if current user is the home team manager
    if current_user.id != team_manager.user_id:
        raise HTTPException(
            status_code=404, detail=f"Current user is not the home team manager")
    # remove match referee
    return remove_match_referee(match)
