from fastapi import APIRouter, Depends, HTTPException, Security
from ..dependencies import oauth2_scheme, get_current_active_user, get_player, get_team, get_team_player, get_match, get_match_player, update_match_player
from ..models import User, MatchPlayerLink
from typing import List


####################################### Matches Section ######################################################################################
matches_router = APIRouter(prefix="/matches",
                           tags=["Matches"],
                           dependencies=[Depends(oauth2_scheme)],
                           responses={404: {"description": "Match Not found"}},)


# matches root
@matches_router.get("/")
async def read_root(current_user: User = Security(get_current_active_user, scopes=["matches"])):
    return{"Welcome to Team Up Matches Section"}


# rate team player
@matches_router.put("/rate_team_player/{team_name}/{player_username}", response_model=List[MatchPlayerLink])
async def rate_team_player(player_username: str, team_name: str, match_id: int, player_rating: int, current_user: User = Security(get_current_active_user, scopes=["matches"])):
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"{player_username} has no player profile")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found!")
    # check if player is in team
    team_player = get_team_player(player, team)
    if not team_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username {player_username} is not in team!")
    # check if current user is in the team
    current_team_player = get_team_player(player, team)
    if not current_team_player:
        raise HTTPException(
            status_code=404, detail=f"Current user is not in team!")
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with id {match_id} not found!")
    # check if player is in match
    match_player = get_match_player(match, team_player)
    if not match_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username {player_username} not found in match!")
    # check if current user is in the match
    if not get_match_player(match, current_team_player):
        raise HTTPException(
            status_code=404, detail=f"Current user is not in match!")
    # Check if the team player rating is between 0 and 5
    if player_rating < 0 or player_rating > 5:
        raise HTTPException(
            status_code=400, detail="Player rating must be between 0 and 5")
    # Calculate the average rating and update the rating count
    player_rating_count = match_player.player_rating_count + 1
    player_rating_total = match_player.player_rating * match_player.player_rating_count
    player_rating_total += player_rating
    player_rating_average = player_rating_total / player_rating_count
    player_rating_average = round(player_rating_average, 2)
    # Update the team player rating
    team_player_update = MatchPlayerLink(match_id=match.match_id, player_id=player.player_id,
                                         player_rating_count=player_rating_count, player_rating=player_rating_average)
    return update_match_player(team_player_update)
