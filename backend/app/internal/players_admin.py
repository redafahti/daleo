from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_user, get_current_active_admin, all_players, create_player, get_player, get_players_in_radius, get_players_by_position_in_radius, get_players_by_rating_radius, get_players_by_rating, update_player, delete_player
from ..models import User, PlayerRead, PlayerCreate, PlayerUpdate
from typing import List


########################### Player admin Section ###########################################################################################
players_admin_router = APIRouter(
    prefix="/players_admin",
    tags=["Players Admin"],
    dependencies=[Depends(oauth2_scheme)],
    responses={418: {"description": "I'm an Administrator"}},)


# read all players
@players_admin_router.get("/get_players", response_model=List[PlayerRead])
async def get_all_players(current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    players = all_players()
    if not players:
        raise HTTPException(
            status_code=404, detail=f"No players found")
    return players


# create player
@players_admin_router.post("/create_player/{username}", response_model=PlayerRead)
async def create_new_player(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if user exists
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username: {username} not found")
    # check if player already exists
    if user.player_id:
        raise HTTPException(
            status_code=404, detail=f"User with username: {username} already has a player profile")
    # check if player has all the required fields
    new_player = PlayerCreate(username=username, user_id=user.id)
    return create_player(new_player)


# get player
@players_admin_router.get("/get_player/{player_username}", response_model=PlayerRead)
async def get_player_profile(player_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} not found")
    return player


# find players by location radius
@players_admin_router.get("/find_players_by_radius/{longitude}/{latitude}/{radius}", response_model=List[PlayerRead])
async def find_players_by_radius(longitude: float, latitude: float, radius: float, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    players = get_players_in_radius(
        longitude=longitude, latitude=latitude, radius=radius)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"No players found in radius")
    return players


# find players by favorite position and location radius
@players_admin_router.get("/find_players_by_position_radius/{favorite_position}/{longitude}/{latitude}/{radius}", response_model=List[PlayerRead])
async def find_players_by_position_in_my_radius(favorite_position: str, longitude: float, latitude: float, radius: float, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    players = get_players_by_position_in_radius(
        longitude=longitude, latitude=latitude, favorite_position=favorite_position, radius=radius)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"No players found in radius")
    return players


# find players by rating and location radius
@players_admin_router.get("/find_players_by_rating_radius/{rating}/{longitude}/{latitude}/{radius}", response_model=List[PlayerRead])
async def find_players_by_rating_in_my_radius(rating: int, longitude: float, latitude: float, radius: float, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    players = get_players_by_rating_radius(
        rating=rating, longitude=longitude, latitude=latitude, radius=radius)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"No players found in radius")
    return players


# get player's rating count and rating
@players_admin_router.get("/get_player_rating/{player_username}")
async def get_player_rating(player_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} not found")
    # update player's ratings
    updated_player = update_player_rating(player)
    if not updated_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} has no ratings")
    return {updated_player.total_rating_count, updated_player.total_rating}


# get players by rating
@players_admin_router.get("/get_players_by_rating/{rating}", response_model=List[PlayerRead])
async def find_players_by_rating(rating: int, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return get_players_by_rating(rating)


# update player
@players_admin_router.put("/update_player/{player_username}", response_model=PlayerRead)
async def update_player_profile(player_username: str, player_height: int | None = None, player_weight: int | None = None, player_foot: str | None = None, favorite_position: str | None = None, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"User: {player_username} has no player profile")
    # check if player fields are valid
    player_update = PlayerUpdate(username=player_username, player_height=player_height,
                                 player_weight=player_weight, player_foot=player_foot, favorite_position=favorite_position)
    return update_player(player_update)


# update player rating
@players_admin_router.put("/update_player_rating/{player_username}", response_model=PlayerRead)
async def update_player_rating(player_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"User: {player_username} has no player profile")
    # update player's ratings
    return update_player_rating(player)


# delete player
@players_admin_router.delete("/delete_player/{player_username}")
async def delete_player_profile(player_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # Check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"User: {player_username} has no player profile")
    # delete player
    return delete_player(player)
