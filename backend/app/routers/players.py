from fastapi import APIRouter, Depends, HTTPException, Security
from ..dependencies import oauth2_scheme, get_current_active_user, get_user, create_player, get_player, update_player, update_player_id, get_current_location, check_player_availability, add_player_availability, get_player_availabilities, get_player_availability, update_player_availability, delete_player_availability, delete_all_player_availabilities, update_player_rating, delete_player, get_coach, get_coach_by_id, get_player_coach, update_coach_rating, add_coach_player_request, get_coach_player_request, update_coach_player_request, remove_coach_player_request, add_player_coach, remove_player_coach, get_team, get_player_teams, add_team_player_request, get_team_player_request, remove_team_player_request, add_team_player, get_team_player, update_team_rating, get_team_by_id, update_team_player_request, remove_team_player, get_player_teams_invitations, get_team_player_invitation, update_team_player_invitation, player_captain_teams, update_team_player, get_players_in_radius, get_players_by_position_in_radius, get_players_by_rating_radius, get_players_by_rating
from ..models import User, Player, PlayerCreate, PlayerRead, PlayerAvailability, CoachRead, CoachUpdate, PlayerCoachRequest, PlayerCoachLink, Team, TeamRead, PlayerTeamRequest, PlayerTeamInvitation, TeamPlayerLink
from datetime import date, time, datetime
from typing import List


########################################  Players Main Section  ############################################################################################################
players_router = APIRouter(prefix="/players",
                           tags=["Players"],
                           dependencies=[Depends(oauth2_scheme)],
                           responses={404: {"description": "Players Not found"}},)


# players root
@players_router.get("/")
async def read_root(current_user: User = Security(get_current_active_user, scopes=["players"])):
    return{"Welcome to Team Up Players Section"}


# create my player profile
@players_router.post("/create_player/me", response_model=PlayerRead)
async def create_my_player_profile(player_height: float | None = None, player_weight: float | None = None, player_foot: str | None = None, favorite_position: str | None = None, join_team: bool | None = True, join_match: bool | None = True, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player already exists
    if current_user.player_id:
        raise HTTPException(
            status_code=404, detail=f"User with username: {current_user.username} already has a player profile")
    # get player current location
    player_latitude , player_longitude  = get_current_location()
    # check if player has all the required fields
    new_player = PlayerCreate(username=current_user.username, player_longitude=player_longitude, player_latitude=player_latitude, player_height=player_height,
                              player_weight=player_weight, player_foot=player_foot, favorite_position=favorite_position, join_team=join_team, join_match=join_match, user_id=current_user.id)
    # create player
    return create_player(new_player)


# set player availability
@players_router.post("/update_player_availability/me", response_model=PlayerAvailability)
async def set_my_availability(availabe_from: datetime, available_to: datetime, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # check if player is available
    available = check_player_availability(
        player=player, available_from=availabe_from, available_to=available_to)
    if available == True:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} is already available during that time period")
    # set player availability
    return add_player_availability(player=player, available_from=availabe_from, available_to=available_to)


# get my player profile
@players_router.get("/get_player/me", response_model=PlayerRead)
async def get_my_player_profile(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    return player


# get my rating count and rating
@players_router.get("/get_player_rating/me")
async def get_my_player_rating(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # update player's ratings
    updated_player = update_player_rating(player)
    if not updated_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} has no ratings")
    return {updated_player.total_rating_count, updated_player.total_rating}


# get my availabilities
@players_router.get("/get_player_availabilities/me")
async def get_my_player_availabilities(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # get player availabilities
    availabilities = get_player_availabilities(player)
    if not availabilities:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} has no availabilities")
    return availabilities


# update my player profile
@players_router.put("/update_player/me", response_model=PlayerRead)
async def update_my_player_profile(player_height: int | None = None, player_weight: int | None = None, player_foot: str | None = None, favorite_position: str | None = None, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if current user is a player
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"User: {current_user.username} has no player profile")
    # check if player fields are valid
    player_update = Player(username=player.username, player_id=player.player_id, player_height=player_height,
                           player_weight=player_weight, player_foot=player_foot, favorite_position=favorite_position)
    return update_player(player_update)


# update my geo location
@players_router.put("/update_player_location/me", response_model=PlayerRead)
async def update_my_location(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # get player current location
    player_latitude, player_longitude  = get_current_location()
    player.player_longitude = player_longitude
    player.player_latitude = player_latitude
    return update_player(player)


# update player preference to join a team or match
@players_router.put("/update_player_preference/me", response_model=PlayerRead)
async def update_my_player_preference(join_team: bool | None = None, join_match: bool | None = None, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if current user is a player
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"User: {current_user.username} has no player profile")
    player.join_team = join_team
    player.join_match = join_match
    # get palyer current location
    player_latitude, player_longitude = get_current_location()
    player.player_longitude = player_longitude
    player.player_latitude = player_latitude
    return update_player(player)


# update my availability
@players_router.put("/update_player_availability/me")
async def update_my_availability(available_from: datetime, available_to: datetime, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # get player availibilities
    availability = get_player_availability(player, available_from)
    if not availability:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} has no availabilities at that time")
    availability.available_from = available_from
    availability.available_to = available_to
    return update_player_availability(availability)


# delete my availability
@players_router.delete("/delete_player_availability/me")
async def delete_my_availability(available_from: datetime, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # get player availibilities
    availability = get_player_availability(player, available_from)
    if not availability:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} has no availabilities")
    return delete_player_availability(availability)


# delete all my availabilities
@players_router.delete("/delete_player_availabilities/me")
async def delete_my_availabilities(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    return delete_all_player_availabilities(player)


# delete my player profile
@players_router.delete("/delete_player/me")
async def delete_my_player_profile(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # Check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"User: {current_user.username} has no player profile")
    # check if the palyer has any availabilities
    availabilities = get_player_availabilities(player)
    if availabilities:
        delete_all_player_availabilities(player)
    update_player_id(current_user.id, None)
    # delete player
    return delete_player(player)


####################################### player coach section ######################################################################################
# add a coach request
@players_router.post("/add_coach_request/{coach_username}", response_model=PlayerCoachRequest)
async def add_coach_request(coach_username: str, message: str | None = None, request_date: date | None = None, request_time: time | None = None,  request_expiry_date: date | None = None, request_expiry_time: time | None = None, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} not found")
    # check if the player is the coach's player
    if player.coach_id != coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} is not {coach.username}'s coach")
    # check if the player has a coach request
    if get_coach_player_request(player, coach):
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} has already a coach request")
    return add_coach_player_request(coach, message)


# remove a coach request
@players_router.delete("/remove_coach_request/{coach_username}")
async def remove_coach_request(coach_username: str, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} not found")
    # check if the player is the coach's player
    if player.coach_id != coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} is not {coach.username}'s coach")
    # get player's coach request
    coach_request = get_coach_player_request(player)
    if not coach_request:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} has no coach request")
    return remove_coach_player_request(coach_request)


# Assign my coach
@players_router.post("/assign_my_coach/{coach_username}", response_model=PlayerRead)
async def assign_my_coach(coach_username: str, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} not found")
    # check if user is a player and create a player if not
    player = get_player(current_user.username)
    if not player:
        new_player = PlayerCreate(username=current_user.username)
        player = create_player(new_player)
    # check if coach is already the player coach
    if player.coach_id == coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} is already the player's coach")
    # player can't be the coach himself
    if player.user_id == coach.user_id:
        raise HTTPException(
            status_code=404, detail=f"Coach can't be coaching himself")
    # check if coach has a player request
    coach_request = get_coach_player_request(player, coach)
    if not coach_request:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} has no coach request")
    # check if player has accepted the request
    if coach_request.is_accepted == False:
        raise HTTPException(
            status_code=404, detail=f"Coach has not accepted the player {current_user.username} request")
    # create a player coach instance
    player_coach = PlayerCoachLink(
        player_id=player.player_id, coach_id=coach.coach_id)
    # add player coach
    return add_player_coach(player_coach)


# get my coach
@players_router.get("/get_player_coach/me", response_model=CoachRead)
async def get_my_coach(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username {current_user.username} has no player profile")
    coach = get_player_coach(player)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Player with username {current_user.username} has no coach")
    return coach


# rate my coach
@players_router.put("/rate_my_coach/{rating}", response_model=CoachRead)
async def rate_my_coach(rating: int, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if current user is a player
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"{current_user.username} is not a player")
    # get player's coach
    coach = get_player_coach(player)
    # check if coach exists
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} has no coach")
    # check if the player is the coach's player
    if player.coach_id != coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} is not {coach.username}'s coach")
    # Check if the coach rating is between 0 and 5
    if rating < 0 or rating > 5:
        raise HTTPException(
            status_code=400, detail="Coach rating must be between 0 and 5"
        )
    # Update coach rating
    coach_update = CoachUpdate(username=coach.username, coach_rating=rating)
    # Update coach
    return update_coach_rating(coach_update)


# remove my coach
@players_router.delete("/remove_my_coach", response_model=PlayerRead)
async def remove_my_coach(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"User {current_user.username} has no player profile")
    # check if player has a coach
    coach_player = get_player_coach(player)
    if not coach_player:
        raise HTTPException(
            status_code=404, detail=f"User {current_user.username} has no coach")
    # get coach by ID
    coach = get_coach_by_id(coach_player.coach_id)
    # check if coach has any pending requests from the player and reject it if there is
    coach_request = get_coach_player_request(player, coach)
    if coach_request:
        coach_request.is_accepted = False
        update_coach_player_request(coach_request)
    # remove coach from player
    return remove_player_coach(coach_player)


################# Team Section ######################################################################################
# get my teams
@players_router.get("/get_my_teams", response_model=List[TeamPlayerLink])
async def player_teams(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    teams = get_player_teams(player)
    if not teams:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} has no teams")
    return teams


# add a team request
@players_router.post("/add_team_request/{team_name}", response_model=PlayerTeamRequest)
async def add_team_request(team_name: str, message: str | None = None, request_date: date | None = None, request_time: time | None = None,  request_expiry_date: date | None = None, request_expiry_time: time | None = None, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with username: {team_name} not found")
    # check if the player is already the team player
    if get_team_player(team, player):
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} is already a team player")
    # check if the player already has a team request
    if get_team_player_request(player, team):
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} already has a team request")
    return add_team_player_request(team, message)


# remove a team request
@players_router.delete("/remove_team_request/{team_name}")
async def remove_team_request(team_name: str, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with username: {team_name} not found")
    # check if team request exists
    team_request = get_team_player_request(player, team)
    if not team_request:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} has no team request")
    return remove_team_player_request(team_request)


# get my invitations to join teams
@players_router.get("/get_team_invitations/{team_name}", response_model=List[PlayerTeamInvitation])
async def get_my_teams_invitations(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # check if the player has any invitations to join teams
    invitations = get_player_teams_invitations(player)
    if not invitations:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} has no invitations")
    return invitations


# get my team invitation
@players_router.get("/get_player_invitation/{team_name}/me", response_model=PlayerTeamInvitation)
async def get_player_invitation(team_name: str, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if team exist
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # check if player invitation exists
    player_invite = get_team_player_invitation(player, team)
    if not player_invite:
        raise HTTPException(
            status_code=404, detail=f"Player invitation for {current_user.username} not found")
    return player_invite


# update player team invitation
@players_router.put("/update_player_team_invitation/me", response_model=List[PlayerTeamInvitation])
async def update_my_team_invitation(team_name: str, is_accepted: bool, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"{current_user.username} has no player profile")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} not found")
    # check if player has any team invitations
    player_invitation = get_team_player_invitation(player, team)
    if not player_invitation:
        raise HTTPException(
            status_code=404, detail=f"{current_user.username} has no invitation from {team_name}")
    player_invitation.is_accepted = is_accepted
    return update_team_player_invitation(player_invitation)


# Assign me to a team
@players_router.post("/assign_me_to_team/{team_name}", response_model=PlayerRead)
async def assign_me_to_team(team_name: str, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with username {team_name} not found")
    # check if user is a player and create a player if not
    player = get_player(current_user.username)
    if not player:
        new_player = PlayerCreate(username=current_user.username)
        player = create_player(new_player)
    # check if the player is already a team player
    if get_team_player(team, player):
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} is already a team player")
    # check if team has a player request
    team_request = get_team_player_request(player, team)
    if not team_request:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} has no team request")
    # check if team has accepted the request
    if team_request.is_accepted == False:
        raise HTTPException(
            status_code=404, detail=f"Team has not accepted the player {current_user.username} request")
    # check if the player has an invitation from the team and set is_accepted to true
    team_invitation = get_team_player_invitation(player, team)
    if team_invitation:
        team_invitation.is_accepted = True
        update_team_player_invitation(team_invitation)
    # create a player team instance
    player_team = TeamPlayerLink(
        player_id=player.player_id, team_id=team.team_id)
    # add player team
    return add_team_player(player_team)


# rate my team
@players_router.put("/rate_my_team/{team_name}/{rating}", response_model=TeamRead)
async def rate_my_team(team_name: str, rating: int, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if current user is a player
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"{current_user.username} is not a player")
    # get player's team
    team = get_team(team_name)
    # check if team exists
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team {team_name} not found")
    # check if the player is the team's player
    team_player = get_team_player(team, player)
    if not team_player:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} is not in {team_name}")
    # Check if the team rating is between 0 and 5
    if rating < 0 or rating > 5:
        raise HTTPException(
            status_code=400, detail="Team rating must be between 0 and 5"
        )
    # Update team rating
    team_update = Team(team_id=team.team_id,
                       team_name=team_name, team_rating=rating)
    # Update team
    return update_team_rating(team_update)


# remove me from team
@players_router.delete("/remove_me_from_team/{team_name}", response_model=PlayerRead)
async def remove_my_team(team_name: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"User {current_user.username} has no player profile")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team {team_name} not found")
    # check if player is in the team
    team_player = get_team_player(team, player)
    if not team_player:
        raise HTTPException(
            status_code=404, detail=f"User {current_user.username} has no team")
    # get team by ID
    team = get_team_by_id(team_player.team_id)
    # check if team has any pending requests from the player and reject it if there is
    team_request = get_team_player_request(player, team)
    if team_request:
        team_request.is_accepted = False
        update_team_player_request(team_request)
    # check if team has any pending invitations from the player and reject it if there is
    team_invitation = get_team_player_invitation(player, team)
    if team_invitation:
        team_invitation.is_accepted = False
        update_team_player_invitation(team_invitation)
    # remove team from player
    return remove_team_player(team_player)


# get teams where i am captain
@players_router.get("/get_player_captain_teams/me", response_model=List[TeamPlayerLink])
async def get_player_captain_teams(current_user: User = Security(get_current_active_user, scopes=["players"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    teams = player_captain_teams(player)
    if not teams:
        raise HTTPException(
            status_code=404, detail=f"Player {current_user.username} is not a captain in any team")
    return teams


# remove me as team captain
@players_router.put("/remove_me_as_team_captain/{team_name}", response_model=TeamPlayerLink)
async def remove_team_captain(team_name: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if player exists
    player = get_player(current_user.username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} not found")
    # check if player is not the team captain
    team_player = get_team_player(player, team)
    if not team_player.is_captain == True:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {current_user.username} is not the team captain")
    team_player = TeamPlayerLink(
        team_id=team.team_id, player_id=player.player_id, is_captain=False)
    return update_team_player(team_player)


################# Player Access #####################################################################################################
# find players by location radius
@players_router.get("/find_players_by_radius/{radius}", response_model=List[PlayerRead])
async def find_players_by_radius(radius: float, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # get user's current location
    user_latitude, user_longitude = get_current_location()
    # get players in radius from user's current location
    players = get_players_in_radius(
        longitude=user_longitude, latitude=user_latitude, radius=radius)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"No players found in radius")
    return players


# find players by favorite position and location radius
@players_router.get("/find_players_by_position_radius/{favorite_position}/{radius}", response_model=List[PlayerRead])
async def find_players_by_position_in_my_radius(favorite_position: str, radius: float, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # get user's current location
    user_latitude, user_longitude = get_current_location()
    players = get_players_by_position_in_radius(
        longitude=user_longitude, latitude=user_latitude, favorite_position=favorite_position, radius=radius)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"No players found in radius")
    return players


# find players by rating and location radius
@players_router.get("/find_players_by_rating_radius/{rating}/{radius}", response_model=List[PlayerRead])
async def find_players_by_rating_in_my_radius(rating: int, radius: float, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # get user's current location
    user_latitude, user_longitude = get_current_location()
    players = get_players_by_rating_radius(
        rating=rating, longitude=user_longitude, latitude=user_latitude, radius=radius)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"No players found in radius")
    return players


# get player's rating count and rating
@players_router.get("/get_player_rating/{player_username}")
async def get_player_rating(player_username: str, current_user: User = Security(get_current_active_user, scopes=["players"])):
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
@players_router.get("/get_players_by_rating/{rating}", response_model=List[PlayerRead])
async def find_players_by_rating(rating: int, current_user: User = Security(get_current_active_user, scopes=["players"])):
    # get players by rating
    players = get_players_by_rating(rating)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"No players found with rating: {rating}")
    return players
