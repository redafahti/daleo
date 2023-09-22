from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_admin, get_player, get_current_location, update_player, get_stadiums_within_radius, get_stadium_home_teams
from ..models import User, TeamRead, PlayerUpdate
from typing import List


################################## Stadium Players Section ##################################################################################################
stadium_players_router = APIRouter(prefix="/stadium_players",
                                   tags=["Stadium Players"],
                                   dependencies=[Depends(oauth2_scheme)],
                                   responses={404: {"description": "Stadium players Not found"}},)


# find teams by home stadium location
@stadium_players_router.get("/find_team_by_location/{radius}", response_model=List[TeamRead])
async def find_teams_by_location(username: str, radius: float, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if player exists
    player = get_player(username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} not found")
    # get player current location
    player_latitude, player_longitude = get_current_location()
    player_update = PlayerUpdate(username=username,
                                 player_latitude=player_latitude, player_longitude=player_longitude)
    updated_player = update_player(player_update)
    # find stadiums in radius
    radius_stadiums = get_stadiums_within_radius(
        updated_player.player_longitude, updated_player.player_latitude, radius=radius)
    # get stadium home teams
    for stadium in radius_stadiums:
        return get_stadium_home_teams(stadium)
