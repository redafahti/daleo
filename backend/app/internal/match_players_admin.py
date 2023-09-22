from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_user, get_player, get_player_matches, get_match, get_match_player, get_match_player_invitation, get_match_player_invitations
from ..models import User, MatchPlayerLink, PlayerMatchInvitation
from typing import List
from datetime import date, time


###################################### Player matches section #######################################################################################################
match_players_router = APIRouter(prefix="/match_players",
                                 tags=["Match Players"],
                                 dependencies=[Depends(oauth2_scheme)],
                                 responses={404: {"description": "Match player Not found"}},)


# get player's matches
@match_players_router.get("/get_player_matches/{username}", response_model=List[MatchPlayerLink])
async def read_player_matches(username: str, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} not found")
    matches = get_player_matches(player)
    if not matches:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} has no matches")
    return matches


# get player match
@match_players_router.get("/get_player_match/{match_id}/{username}", response_model=MatchPlayerLink)
async def read_player_match(match_id: int, username: str, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} not found")
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with id: {match_id} not found")
    # check if player is in match
    if not get_match_player(player, match):
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} is not in match with id: {match_id}")
    return get_match_player(player, match)


############### Player Match Invitation #########################################################################################################################################################
# Create player match invitation using player id and match id
@match_players_router.post("/create_player_match_invitation/{player_name}/{match_id}", response_model=PlayerMatchInvitation)
async def create_player_match_invitation(player_name: str, match_id: int, invitation_date: date | None = None, invitation_time: time | None = None, invitation_expiry_date: date | None = None, invitation_expiry_time: time | None = None, current_user: User = Security(get_current_active_user, scopes=["admin", "invitations"])):
    if current_user:
        # check if player exists
        player = get_player(player_name)
        if not player:
            raise HTTPException(
                status_code=404, detail=f"Player with ID: {player_name} not found")
        # check if match exists
        match = get_match(match_id)
        if not match:
            raise HTTPException(
                status_code=404, detail=f"Match with ID: {match_id} not found")
        # check if player match invitation exists
        player_match_invitation = get_match_player_invitation(
            player_name=player_name, match_id=match_id)
        if player_match_invitation:
            raise HTTPException(
                status_code=404, detail=f"Player with name: {player_name} has already been invited to match with ID: {match_id}")
        # create player match invitation
        new_player_match_invitation = PlayerMatchInvitation(player_name=player_name, match_id=match_id, invitation_date=invitation_date,
                                                            invitation_time=invitation_time, invitation_expiry_date=invitation_expiry_date, invitation_expiry_time=invitation_expiry_time)
        # add player match invitation to database
        create_player_match_invitation(new_player_match_invitation)
        return new_player_match_invitation
    else:
        raise HTTPException(
            status_code=404, detail=f"You are not authorized to create player match invitation")


# Read player match invitation
@match_players_router.get("/get_player_match_invitation", response_model=PlayerMatchInvitation)
async def read_player_match_invitation(player_name: str, match_id: int, current_user: User = Security(get_current_active_user, scopes=["admin", "invitations"])):
    if current_user:
        # check if player exists
        player = get_player(player_name)
        if not player:
            raise HTTPException(
                status_code=404, detail=f"Player with name: {player_name} not found")
        # check if match exists
        match = get_match(match_id=match_id)
        if not match:
            raise HTTPException(
                status_code=404, detail=f"Match with ID: {match_id} not found")
        # check if player match invitation exists
        player_match_invitation = get_match_player_invitation(
            player_name=player_name, match_id=match_id)
        if not player_match_invitation:
            raise HTTPException(
                status_code=404, detail=f"Player with name: {player_name} has NOT been invited to match with ID: {match_id}")
        return player_match_invitation
    else:
        raise HTTPException(
            status_code=404, detail=f"You are not authorized to view player match invitation")


# Read all player match invitations by player name
@match_players_router.get("/get_player_match_invitations/{player_name}", response_model=List[PlayerMatchInvitation])
async def get_player_match_invitations_by_player_id(player_name: str, current_user: User = Security(get_current_active_user, scopes=["admin", "invitations"])):
    if current_user:
        # check if player exists
        player = get_player(player_name)
        if not player:
            raise HTTPException(
                status_code=404, detail=f"Player with name: {player_name} not found")
        # get all player match invitations
        player_match_invitations = get_match_player_invitations(player_name)
        return player_match_invitations
    else:
        raise HTTPException(
            status_code=404, detail=f"You are not authorized to view player match invitations")


# Read all player match invitations by match id
@match_players_router.get("/get_player_match_invitations_by_match_id/{match_id}", response_model=List[PlayerMatchInvitation])
async def get_player_match_invitations_by_match_id(match_id: int, current_user: User = Security(get_current_active_user, scopes=["admin", "invitations"])):
    if current_user:
        # check if match exists
        match = get_match(match_id)
        if not match:
            raise HTTPException(
                status_code=404, detail=f"Match with ID: {match_id} not found")
        # get all player match invitations
        player_match_invitations = get_match_player_invitations(match_id)
        return player_match_invitations
    else:
        raise HTTPException(
            status_code=404, detail=f"You are not authorized to view player match invitations")
