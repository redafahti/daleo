from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_user, all_players_coaches, get_coach, get_coach_players, get_player, get_player_coach, create_coach, create_player, get_coach_player_request, add_player_coach, get_coach_by_id, update_coach_player_request, remove_player_coach
from ..models import User, CoachRead, PlayerRead, CoachCreate, PlayerCreate, PlayerCoachLink
from typing import List


####################################  Player Coaches Section  ############################################################################################################
player_coach_router = APIRouter(prefix="/player_coach",
                                tags=["Player Coach"],
                                dependencies=[Depends(oauth2_scheme)],
                                responses={404: {"description": "Player Coach Not found"}},)


# get all players coaches
@player_coach_router.get("/get_all_players_coaches", response_model=List[CoachRead])
async def read_all_players_coaches(current_user: User = Security(get_current_active_user, scopes=["admin"])):
    coaches = all_players_coaches()
    if not coaches:
        raise HTTPException(
            status_code=404, detail=f"No players coaches found")
    return coaches


# get coach's players
@player_coach_router.get("/get_coach_players/{coach_username}", response_model=List[PlayerRead])
async def read_coach_players(coach_username: str, current_user: User = Security(get_current_active_user, scopes=["admin"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} not found")
    players = get_coach_players(coach)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} has no players")
    return players


# get player's coach
@player_coach_router.get("/get_player_coach/{player_username}", response_model=CoachRead)
async def read_player_coach(player_username: str, current_user: User = Security(get_current_active_user, scopes=["admin"])):
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username {player_username} has no player profile")
    coach = get_player_coach(player)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Player with username {player_username} has no coach")
    return coach


# Assign coach to player
@player_coach_router.put("/assign_coach_to_player/{player_username}/{coach_username}", response_model=PlayerRead)
async def assign_coach_to_player(player_username: str, coach_username: str, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if coach exists and create coach if not
    coach = get_coach(coach_username)
    if not coach:
        new_coach = CoachCreate(username=coach_username)
        coach = create_coach(new_coach)
    # check if user is a player and create a player if not
    player = get_player(player_username)
    if not player:
        new_player = PlayerCreate(username=player_username)
        player = create_player(new_player)
    # check if coach is already the player coach
    if player.coach_id == coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} is already the player's coach")
    # player can't be the coach himself
    if player.user_id == coach.user_id:
        raise HTTPException(
            status_code=404, detail=f"Coach can't be coaching himself")
    # check if player has a coach request
    coach_request = get_coach_player_request(player, coach)
    if not coach_request:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} has no coach request")
    # check if coach has accepted the request
    if coach_request.is_accepted == False:
        raise HTTPException(
            status_code=404, detail=f"Coach has not accepted the player {current_user.username} request")
    # create a player coach instance
    player_coach = PlayerCoachLink(
        player_id=player.player_id, coach_id=coach.coach_id)
    # add player coach
    return add_player_coach(player_coach)


# remove coach from player
@player_coach_router.put("/remove_player_coach/me", response_model=PlayerRead)
async def remove_player_from_coach(player_username: str, current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"User {player_username} has no player profile")
    # check if player has a coach
    coach_player = get_player_coach(player)
    if not coach_player:
        raise HTTPException(
            status_code=404, detail=f"User {player_username} has no coach")
    # get coach by ID
    coach = get_coach_by_id(coach_player.coach_id)
    # check if coach has any pending requests from the player and reject it if there is
    coach_request = get_coach_player_request(player, coach)
    if coach_request:
        coach_request.is_accepted = False
        update_coach_player_request(coach_request)
    # remove coach from player
    return remove_player_coach(coach_player)
