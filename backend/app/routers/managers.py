from fastapi import APIRouter, Depends, HTTPException, Security
from ..dependencies import oauth2_scheme, get_current_active_user, create_manager, get_manager, get_user, update_manager, get_manager_teams, get_team_manager, assign_team_manager, delete_manager, get_team, create_team, update_team, delete_team, get_stadium, get_players_in_radius, add_team_player_invitation, get_players_by_position_in_radius, get_players_by_rating, get_team_players_requests, get_team_player_request, get_player, player_join_team, update_match, update_team_player_request, get_team_players, get_team_player, update_team_player_invitation, get_team_player_invitation, add_team_player, remove_team_player, get_coach, get_team_coach_request, get_team_coach, add_team_coach, add_team_coach_request, remove_team_coach_request, update_coach_rating, get_coach_by_id, update_team_coach_request, remove_team_coach, get_team_captain, update_team_player, remove_team_player_invitation, get_stadium_available_pitches, get_match, create_match, assign_match_home_team, assign_match_away_team, check_team_availability, get_team_match_invitation, get_match_team_request, update_match_team_request, add_team_match_invitation, get_stadium_teams, remove_team_match_invitation, get_match_teams_requests, add_match_team, get_match_team, remove_match_team
from ..models import User, ManagerCreate, ManagerRead, ManagerUpdate, TeamRead, TeamCreate, TeamUpdate, CoachRead, TeamCoachLink, TeamCoachRequest, PlayerTeamInvitation, PlayerTeamRequest, TeamPlayerLink, CoachUpdate, MatchTeamLink, MatchCreate, TeamMatchInvitation, TeamMatchRequest
from typing import List
from datetime import datetime, timedelta, date, time


################################  Managers Main Section  ############################################################################################################
managers_router = APIRouter(prefix="/managers",
                            tags=["Managers"],
                            dependencies=[Depends(oauth2_scheme)],
                            responses={404: {"description": "Managers Not found"}},)


# managers root
@managers_router.get("/")
async def read_root(current_user: User = Security(get_current_active_user, scopes=["managers"])):
    return{"Welcome to Team Up Managers Section"}


# create my manager profile
@managers_router.post("/create_manager_profile/me", response_model=ManagerRead)
async def create_my_manager_profile(current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if user is already a manager
    if current_user.manager_id:
        raise HTTPException(
            status_code=404, detail=f"User with username: {current_user.username} already has a manager profile")
    # check if user has all the required fields
    new_manager = ManagerCreate(
        username=current_user.username, user_id=current_user.id, manager_rating=0, manager_rating_count=0)
    return create_manager(new_manager)


# get my manager profile
@managers_router.get("/get_manager_profile/me", response_model=ManagerRead)
async def get_my_manager_profile(current_user: User = Security(get_current_active_user, scopes=["managers"])):
    manager = get_manager(current_user.username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {current_user.username} not found")
    return manager


# update my manager profile
@managers_router.put("/update_manager_profile/me", response_model=ManagerRead)
async def update_my_manager_profile(season_rate: int | None = None, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if current user is a manager
    manager = get_manager(current_user.username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"User: {current_user.username} has no manager profile")
    # check if manager fields are valid
    manager_update = ManagerUpdate(
        username=current_user.username, manager_season_rate=season_rate)
    return update_manager(manager_update)


# delete my manager profile
@managers_router.delete("/delete_manager_profile/me", response_model=ManagerRead)
async def delete_my_manager_profile(current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if current user is a manager
    manager = get_manager(current_user.username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"User: {current_user.username} has no manager profile")
    # get manager teams
    teams = get_manager_teams(manager)
    if teams is not None:
        raise HTTPException(
            status_code=404, detail=f"User: {current_user.username} has teams, assign a new manager to the teams before deleting")
    # remove manager
    return delete_manager(manager)


####################################  Teams manager section ######################################################################################################
# create team
@managers_router.post("/create_team/{team_name}", response_model=TeamRead)
async def create_new_team(team_name: str, team_logo: str | None = None, team_home_color_jersey: str | None = None, team_away_color_jersey: str | None = None, team_home_color_shorts: str | None = None, team_away_color_shorts: str | None = None, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team already exists
    team = get_team(team_name)
    if team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} already exists")
    # assign current user as team manager and create a manager profile for the user if not already created
    manager = get_manager(current_user.username)
    if not manager:
        manager_create = ManagerCreate(
            username=current_user.username, user_id=current_user.id)
        manager = create_manager(manager_create)
    # check if team has all the required fields
    new_team = TeamCreate(team_name=team_name, team_logo=team_logo, team_home_color_jersey=team_home_color_jersey, team_away_color_jersey=team_away_color_jersey,
                          team_home_color_shorts=team_home_color_shorts, team_away_color_shorts=team_away_color_shorts, manager_id=manager.manager_id, team_rating=0, team_rating_count=0)
    return create_team(new_team)


# read the teams I manage
@managers_router.get("/manager_teams/me", response_model=List[TeamRead])
async def get_my_teams(current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if current user is a manager
    manager = get_manager(current_user.username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {current_user.username} not found")
    # get manager teams
    teams = get_manager_teams(manager)
    if not teams:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {current_user.username} has no teams")
    return teams


# update a team I manage
@managers_router.put("/update_team/{team_name}", response_model=TeamRead)
async def update_my_team(team_name: str, team_logo: str | None = None, team_home_color_jersey: str | None = None, team_away_color_jersey: str | None = None, team_home_color_shorts: str | None = None, team_away_color_shorts: str | None = None, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if current user is a manager
    manager = get_manager(current_user.username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {current_user.username} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if the current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.manager_id != manager.manager_id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    # check if team has all the required fields
    team_update = TeamUpdate(team_name=team_name, team_logo=team_logo, team_home_color_jersey=team_home_color_jersey, team_away_color_jersey=team_away_color_jersey,
                             team_home_color_shorts=team_home_color_shorts, team_away_color_shorts=team_away_color_shorts)
    return update_team(team_update)


# assign new Manager to my team
@managers_router.put("/assign_team_manager/{team_name}/{manager_username}", response_model=TeamRead)
async def assign_my_team_manager(team_name: str, manager_username: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if current user is a manager
    manager = get_manager(current_user.username)
    if not manager:
        raise HTTPException(
            status_code=404, detail=f"Manager with username {current_user.username} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.manager_id != manager.manager_id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    # check if new manager is a user
    user = get_user(manager_username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {manager_username} not found")
    # check if new manager is a manager and create one if not
    manager = get_manager(manager_username)
    if not manager:
        new_manager = ManagerCreate(username=manager_username, user_id=user.id)
        manager = create_manager(new_manager)
    # check if manager already the team manager
    if manager.manager_id == team.manager_id:
        raise HTTPException(
            status_code=400, detail=f"User {manager_username} is already {team_name} manager")
    return assign_team_manager(manager, team)


# delete my team
@managers_router.delete("/delete_team/{team_name}")
async def delete_my_team(team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    # check if current user is the team manage
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    return delete_team(team_name)


####################################### team coach manager section ######################################################################################
# add a team coach request
@managers_router.post("/add_my_team_coach_request/{coach_username}", response_model=TeamCoachRequest)
async def add_my_team_coach_request(coach_username: str, message: str | None = None, request_date: date | None = None, request_time: time | None = None,  request_expiry_date: date | None = None, request_expiry_time: time | None = None, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if team exists
    team = get_team(current_user.username)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with username: {current_user.username} not found")
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} not found")
    # check if the team is the coach's team
    if team.coach_id != coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Team {current_user.username} is not {coach.username}'s coach")
    # check if the team has a coach request
    if get_team_coach_request(team, coach):
        raise HTTPException(
            status_code=404, detail=f"Team {current_user.username} has already a coach request")
    return add_team_coach_request(coach, message)


# remove a coach team request
@managers_router.delete("/remove_my_team_coach_request/{coach_username}")
async def remove_my_team_coach_request(coach_username: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if team exists
    team = get_team(current_user.username)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with username: {current_user.username} not found")
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} not found")
    # check if the team is the coach's team
    if team.coach_id != coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Team {current_user.username} is not {coach.username}'s coach")
    # get team's coach request
    coach_request = get_team_coach_request(team)
    if not coach_request:
        raise HTTPException(
            status_code=404, detail=f"Team {current_user.username} has no coach request")
    return remove_team_coach_request(coach_request)


# Assign team coach
@managers_router.post("/assign_my_team_coach/{coach_username}", response_model=TeamRead)
async def assign_my_team_coach(coach_username: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} not found")
    # check if user is a team and create a team if not
    team = get_team(current_user.username)
    if not team:
        new_team = TeamCreate(username=current_user.username)
        team = create_team(new_team)
    # check if coach is already the team coach
    if team.coach_id == coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} is already the team's coach")
    # team can't be the coach himself
    if team.user_id == coach.user_id:
        raise HTTPException(
            status_code=404, detail=f"Coach can't be coaching himself")
    # check if coach has a team request
    coach_request = get_team_coach_request(team, coach)
    if not coach_request:
        raise HTTPException(
            status_code=404, detail=f"Team {current_user.username} has no coach request")
    # check if team has accepted the request
    if coach_request.is_accepted == False:
        raise HTTPException(
            status_code=404, detail=f"Coach has not accepted the team {current_user.username} request")
    # create a team coach instance
    team_coach = TeamCoachLink(
        team_id=team.team_id, coach_id=coach.coach_id)
    # add team coach
    return add_team_coach(team_coach)


# get my team coach
@managers_router.get("/get_my_team_coach/me", response_model=CoachRead)
async def get_my_team_coach(current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if team exists
    team = get_team(current_user.username)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with username {current_user.username} has no team profile")
    coach = get_team_coach(team)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Team with username {current_user.username} has no coach")
    return coach


# rate my team coach
@managers_router.put("/rate_my_team_coach/{rating}", response_model=CoachRead)
async def rate_my_team_coach(rating: int, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if current user is a team
    team = get_team(current_user.username)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"{current_user.username} is not a team")
    # get team's coach
    coach = get_team_coach(team)
    # check if coach exists
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Team {current_user.username} has no coach")
    # check if the team is the coach's team
    if team.coach_id != coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Team {current_user.username} is not {coach.username}'s coach")
    # Check if the coach rating is between 0 and 5
    if rating < 0 or rating > 5:
        raise HTTPException(
            status_code=400, detail="Coach rating must be between 0 and 5"
        )
    # Update coach rating
    coach_update = CoachUpdate(username=coach.username, coach_rating=rating)
    # Update coach
    return update_coach_rating(coach_update)


# remove team coach
@managers_router.delete("/remove_team_coach/{team_name}", response_model=TeamRead)
async def remove_my_team_coach(team_name: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team {current_user.username} not found")
    # check if team has a coach
    coach_team = get_team_coach(team)
    if not coach_team:
        raise HTTPException(
            status_code=404, detail=f"User {current_user.username} has no coach")
    # get coach by ID
    coach = get_coach_by_id(coach_team.coach_id)
    # check if coach has any pending requests from the team and reject it if there is
    coach_request = get_team_coach_request(team, coach)
    if coach_request:
        coach_request.is_accepted = False
        update_team_coach_request(coach_request)
    # remove coach from team
    return remove_team_coach(coach_team)


######################################## team players manager section #####################################################################################
# get my team players
@managers_router.get("/get_my_team_players/{team_name}", response_model=List[TeamPlayerLink])
async def get_my_team_players(team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    players = get_team_players(team)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"No players assigned to team {team_name}")
    return players


# get my team player
@managers_router.get("/get_my_team_player/{username}/{team_name}", response_model=TeamPlayerLink)
async def get_my_team_player(username: str, team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if player exists
    player = get_player(username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    # get player's team
    team_player = get_team_player(team, player)
    if not team_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} is not assigned to {team.team_name} team")
    return team_player


# invite player to my team
@managers_router.post("/create_player_team_invitation/{team_name}/{player_username}", response_model=PlayerTeamInvitation)
async def create_player_team_invitation(team_name: str, player_username: str, message: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} not found")
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} not found")
    # check if player is already in team
    team_player = get_team_player(player)
    if team_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} is already in team with name: {team_name}")
    # check if the player is willing to join a team
    if player_join_team(player) == False:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} is not willing to join a team")
    # check if the current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    # check if player is already invited to team
    player_team_invitation = get_team_player_invitation(player, team)
    if player_team_invitation:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} has already been invited to team with name: {team_name}")
    # check if player has a team request and update it to accepted
    player_team_request = get_team_player_request(player, team)
    if player_team_request:
        player_team_request.is_accepted = True
        update_team_player_request(player_team_request)
    # create player invitation
    new_player_invitation = PlayerTeamInvitation(player_id=player.player_id, team_id=team.team_id, message=message, invitation_date=date.today(
    ), invitation_time=datetime.now().time(), invitation_expiry_date=date.today() + timedelta(days=7), invitation_expiry_time=datetime.now().time())
    # add player invitation to database
    add_team_player_invitation(new_player_invitation)
    return new_player_invitation


# invite players to my team by location
@managers_router.get("/invite_players_by_location/{team_name}/{radius}", response_model=List[PlayerTeamInvitation])
async def invite_players_by_location(team_name: str, radius: float, message: str | None = None, invitation_expiry_days: int | None = None, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    # check if the current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    # check if team has a home stadium
    home_stadium = get_stadium(team.home_stadium_id)
    if not home_stadium:
        raise HTTPException(
            status_code=400, detail=f"Team with team name: {team_name} does not have a home stadium")
    stadium_longitude = home_stadium.stadium_longitude
    stadium_latitude = home_stadium.stadium_latitude
    # get current date
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    # calculate the expiry date and time if invitation expiry days is set
    if invitation_expiry_days:
        expiry_date = current_date + timedelta(days=invitation_expiry_days)
        expiry_time = current_time + timedelta(hours=24)
    # find players within radius from home stadium
    players = get_players_in_radius(
        stadium_longitude, stadium_latitude, radius)
    for player in players:
        # check if player is willing to join a team
        if player_join_team(player) == True:
            player_invite = PlayerTeamInvitation(
                player_id=player.player_id, team_id=team.team_id, message=message, invitation_date=current_date, invitation_time=current_time, invitation_expiry_date=expiry_date, invitation_expiry_time=expiry_time)
            return add_team_player_invitation(player_invite)


# Invite players to my team by favorite position and location radius
@managers_router.get("/invite_players_by_position/{team_name}/{favorite_position}/{radius}", response_model=List[PlayerTeamInvitation])
async def invite_players_by_position(team_name: str, favorite_position: str, radius: float, message: str | None = None, invitation_expiry_days: int | None = None, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    # check if current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    # check if team has a home stadium
    home_stadium = get_stadium(team.home_stadium_id)
    if not home_stadium:
        raise HTTPException(
            status_code=400, detail=f"Team with team name: {team_name} does not have a home stadium")
    stadium_longitude = home_stadium.stadium_longitude
    stadium_latitude = home_stadium.stadium_latitude
    # get current date
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    # calculate the expiry date and time if invitation expiry days is set
    if invitation_expiry_days:
        expiry_date = current_date + timedelta(days=invitation_expiry_days)
        expiry_time = current_time + timedelta(hours=24)
    expiry_date = current_date + timedelta(days=7)
    expiry_time = current_time + timedelta(hours=24)
    # find players within radius from home stadium
    players = get_players_by_position_in_radius(
        longitude=stadium_longitude, latitude=stadium_latitude, favorite_position=favorite_position, radius=radius)
    for player in players:
        # check if player is willing to join a team
        if player_join_team(player) == True:
            player_invite = PlayerTeamInvitation(
                player_id=player.player_id, team_id=team.team_id, message=message, invitation_date=current_date, invitation_time=current_time, invitation_expiry_date=expiry_date, invitation_expiry_time=expiry_time)
            return add_team_player_invitation(player_invite)


# invite players to my team by rating and location radius
@managers_router.get("/invite_players_by_rating", response_model=List[PlayerTeamInvitation])
async def invite_players_by_rating(team_name: str, rating: int, radius: float, message: str | None = None, invitation_expiry_days: int | None = None, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    # check if current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    # check if team has a home stadium
    home_stadium = get_stadium(team.home_stadium_id)
    if not home_stadium:
        raise HTTPException(
            status_code=400, detail=f"Team with team name: {team_name} does not have a home stadium")
    stadium_longitude = home_stadium.stadium_longitude
    stadium_latitude = home_stadium.stadium_latitude
    # get current date
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    # calculate the expiry date and time if invitation expiry days is set
    if invitation_expiry_days:
        expiry_date = current_date + timedelta(days=invitation_expiry_days)
        expiry_time = current_time + timedelta(hours=24)
    expiry_date = current_date + timedelta(days=7)
    expiry_time = current_time + timedelta(hours=24)
    # find players with rating and within radius from home stadium
    players = get_players_by_rating(
        longitude=stadium_longitude, latitude=stadium_latitude, rating=rating, radius=radius)
    for player in players:
        # check if player is willing to join a team
        if player_join_team(player) == True:
            player_invite = PlayerTeamInvitation(
                player_id=player.player_id, team_id=team.team_id, message=message, invitation_date=current_date, invitation_time=current_time, invitation_expiry_date=expiry_date, invitation_expiry_time=expiry_time)
            return add_team_player_invitation(player_invite)


# remove my team player invitation
@managers_router.delete("/remove_my_team_player_invitation/{team_name}/{player_username}", response_model=PlayerTeamInvitation)
async def remove_my_team_player_invitation(team_name: str, player_username: str, message: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} not found")
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} not found")
    # check if player is already in team
    team_player = get_team_player(player)
    if not team_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} is not in team with name: {team_name}")
    # check if the current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    # check if player has a team request and update it to not accpepted
    player_team_request = get_team_player_request(player, team)
    if player_team_request:
        player_team_request.is_accepted = False
        update_team_player_request(player_team_request)
    # get team player invitation
    player_team_invitation = get_team_player_invitation(player, team)
    # remove player invitation
    return remove_team_player_invitation(player_team_invitation)


# get players requests to join my team
@managers_router.get("/get_my_team_players_requests/{team_name}", response_model=List[PlayerTeamRequest])
async def get_my_team_players_requests(team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    requests = get_team_players_requests(team)
    if not requests:
        raise HTTPException(
            status_code=404, detail=f"No player requests for team {team_name} found")
    return requests


# update player request to join my team
@managers_router.put("/update_player_request/{player_username}/{team_name}/{is_accepted}", response_model=PlayerTeamRequest)
async def update_player_request(player_username: str, team_name: str, is_accepted: bool, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username {player_username} not found")
    # check if player request exists
    player_request = get_team_player_request(player, team)
    if not player_request:
        raise HTTPException(
            status_code=404, detail=f"Player request for {player_username} not found")
    # approve player Team Request
    request_approval = PlayerTeamRequest(
        player_request.team_id, player_request.player_id, is_accepted=is_accepted)
    return update_team_player_request(request_approval)


# Add a player to my team
@managers_router.post("/add_my_team_player/{player_username}", response_model=TeamPlayerLink)
async def add_my_team_player(player_username: str, team_name: str, is_captain: bool | None = False, player_position: str | None = None, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"{player_username} has no player profile")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team named: {team_name} not found")
    # check if current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {team_name} manager")
    # check if player is willing to join the team
    if player_join_team(player):
        raise HTTPException(
            status_code=400, detail=f"Player {player_username} is not willing to join a team")
    # check if player is already assigned to the team
    team_player = get_team_player(team, player)
    if team_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} is already assigned to the {team_name} team")
    # check if team player has request
    team_player_request = get_team_player_request(player, team)
    # if team player has request update it
    if team_player_request:
        team_player_request.is_accepted = True
        update_team_player_request(team_player_request)
    # if team player has an invitation update it
    team_player_invitation = get_team_player_invitation(player, team)
    if team_player_invitation:
        team_player_invitation.is_accepted = True
        update_team_player_invitation(team_player_invitation)
    new_team_player = TeamPlayerLink(
        player_id=player.player_id, team_id=team.team_id, is_captain=is_captain, player_position=player_position)
    # update team captain if player is assigned as captain
    if is_captain == True:
        captain_update = TeamUpdate(
            team_name=team.team_name, captain_id=player.player_id)
        update_team(captain_update)
    return add_team_player(new_team_player)


# remove player from my team
@managers_router.put("/remove_my_team_player/{player_username}/{team_name}")
async def remove_my_team_player(player_username: str, team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"{player_username} has no player profile")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if player is assigned to the team
    team_player = get_team_player(player, team)
    if not team_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} is not assigned to team {team_name}")
    # check if player is captain
    if team.captain_id == player.player_id:
        captain_update = TeamUpdate(team_name=team.team_name, captain_id=None)
        update_team(captain_update)
    return remove_team_player(team_player)


#################################### Team Captains manager Section ######################################################################################################
# get my team captain
@managers_router.get("/get_my_team_captain/{team_name}", response_model=TeamPlayerLink)
async def get_my_team_captain(team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    team_captain = get_team_captain(team)
    if not team_captain:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} has no captain")
    return team_captain


# assign my team captain
@managers_router.put("/add_my_team_captain/{username}/{team_name}")
async def add_my_team_captain(username: str, team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if player exists
    player = get_player(username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} not found")
    # check if player is a team player
    team_player = get_team_player(player, team)
    if not team_player:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} is not a team player of team {team_name}")
    # check if player is already team captain
    captain = get_team_captain(team)
    if captain and captain.player_id == player.player_id:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {username} is already the captain of team {team_name}")
    # assign player as team captain
    team_player = TeamPlayerLink(
        team_id=team.team_id, player_id=player.player_id, is_captain=True)
    return update_team_player(team_player)


# remove my team captain
@managers_router.put("/remove_my_team_captain/{team_name}", response_model=TeamPlayerLink)
async def remove_my_team_captain(team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} not found")
    # check if team has a captain
    captain = get_team_captain(team)
    if not captain:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {team_name} has no captain")
    # remove team captain
    team_player = TeamPlayerLink(
        team_id=team.team_id, player_id=captain.player_id, is_captain=False)
    return update_team_player(team_player)


########################## Match Manager Section ######################################################################################################
# create a match
@managers_router.post("/create_match/{team_name}/{stadium}/{match_duration}/{match_start_time}/{teams_size}/{number_of_substitutes}/{match_type}/{match_prize}", response_model=MatchTeamLink)
async def new_match(team_name: str, stadium_id: int, match_duration: int, match_start_time: datetime, teams_size: int, number_of_substitutes: int | None = None, match_type: str | None = None, match_prize: int | None = None, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if home team exists
    home_team = get_team(team_name)
    if not home_team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name {team_name} not found")
    # check if current user is the home team manager
    team_manager = get_team_manager(home_team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"Current user is not the home team manager")
    # check if stadium exists
    stadium = get_stadium(stadium_id)
    if not stadium:
        raise HTTPException(
            status_code=404, detail=f"Stadium with stadium id {stadium_id} not found")
    # check if match start time is valid
    if match_start_time < datetime.now():
        raise HTTPException(
            status_code=404, detail=f"Match start time {match_start_time} is not valid")
    # check if the stadium is available during the match time duration
    available_pitches = get_stadium_available_pitches(
        stadium=stadium, start_time=match_start_time, duration=match_duration)
    if available_pitches < 1:
        raise HTTPException(
            status_code=404, detail=f"Stadium with stadium id {stadium_id} is not available during the match time duration")
    # create match
    new_match = MatchCreate(home_team_name=home_team.team_name, home_team_id=home_team.team_id, match_duration=match_duration, match_start_time=match_start_time,
                            stadium_id=stadium.stadium_id, stadium_name=stadium.stadium_name, teams_size=teams_size, number_of_substitutes=number_of_substitutes, match_type=match_type, match_prize=match_prize)
    match = create_match(new_match)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match was not created")
    # set team to be match home team
    assign_match_home_team(match, home_team)
    # create match team link
    match_home_team = add_match_team(match, home_team, is_home_team=True)
    return match_home_team


# invite team to my match
@managers_router.post("/create_team_match_invitation/{match_id}/{away_team_name}", response_model=TeamMatchInvitation)
async def create_team_match_invitation(match_id: int, away_team_name: str, message: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with ID: {match_id} not found")
    # check if team exists
    away_team = get_team(away_team_name)
    if not away_team:
        raise HTTPException(
            status_code=404, detail=f"Team with name: {away_team_name} not found")
    # check if the team is available for the match
    match_end_time = match.match_start_time + \
        timedelta(minutes=match.match_duration)
    if check_team_availability(away_team, match.match_start_time, match_end_time) == False:
        raise HTTPException(
            status_code=404, detail=f"Team: {away_team} is not available for match at match time")
    # check if the current user is the home team manager
    home_team = get_team(match.home_team_name)
    home_team_manager = get_team_manager(home_team)
    if home_team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {home_team_manager} manager")
    # check if the home team is in the match
    match_team = get_match_team(match, home_team)
    if not match_team:
        raise HTTPException(
            status_code=404, detail=f"Home team: {home_team} is not in the match")
    # check if team is already invited to match
    team_match_invitation = get_team_match_invitation(away_team, match)
    if team_match_invitation:
        raise HTTPException(
            status_code=404, detail=f"Team: {away_team_name} has already been invited to the match")
    # check if team has a match request and update it to accepted
    team_match_request = get_match_team_request(away_team, match)
    if team_match_request:
        team_match_request.is_accepted = True
        update_match_team_request(team_match_request)
    # create team invitation
    new_team_invitation = TeamMatchInvitation(team_id=away_team.team_id, match_id=match.match_id, message=message, invitation_date=date.today(
    ), invitation_time=datetime.now().time(), invitation_expiry_date=date.today() + timedelta(days=7), invitation_expiry_time=datetime.now().time())
    # add team invitation to database
    add_team_match_invitation(new_team_invitation)
    return new_team_invitation


# invite teams to my match by stadium and availability
@managers_router.get("/invite_teams_by_stadium/{match_id}/{stadium_id}", response_model=List[TeamMatchInvitation])
async def invite_teams_by_stadium(match_id: int, stadium_id: int, message: str | None = None, invitation_expiry_days: int | None = None, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with match name: {match_id} not found")
    # check if the current user is the home team manager
    home_team = get_team(match.home_team_name)
    home_team_manager = get_team_manager(home_team)
    if home_team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {home_team_manager} manager")
    # get current date
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    # calculate the expiry date and time if invitation expiry days is set
    if invitation_expiry_days:
        expiry_date = current_date + timedelta(days=invitation_expiry_days)
        expiry_time = current_time + timedelta(hours=24)
    # get stadium teams
    teams = get_stadium_teams(stadium_id)
    match_end_time = match.match_start_time + \
        timedelta(minutes=match.match_duration)
    for team in teams:
        # check if team is available for the match
        if check_team_availability(team, match.match_start_time, match_end_time) == True:
            team_invite = TeamMatchInvitation(
                team_id=team.team_id, match_id=match.match_id, message=message, invitation_date=current_date, invitation_time=current_time, invitation_expiry_date=expiry_date, invitation_expiry_time=expiry_time)
            return add_team_match_invitation(team_invite)


# remove my match team invitation
@managers_router.delete("/remove_my_match_team_invitation/{match_id}/{team_name}", response_model=TeamMatchInvitation)
async def remove_my_match_team_invitation(match_id: int, team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with name: {match_id} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with username: {team_name} not found")
    # check if the current user is the home team manager
    home_team = get_team(match.home_team_name)
    home_team_manager = get_team_manager(home_team)
    if home_team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {home_team_manager} manager")
    # check if team has a match request and update it to not accpepted
    team_match_request = get_match_team_request(team, match)
    if team_match_request:
        team_match_request.is_accepted = False
        update_match_team_request(team_match_request)
    # get match team invitation
    team_match_invitation = get_team_match_invitation(team, match)
    # remove team invitation
    return remove_team_match_invitation(team_match_invitation)


# get teams requests to join my match
@managers_router.get("/get_my_match_teams_requests/{match_id}", response_model=List[TeamMatchRequest])
async def get_my_match_teams_requests(match_id: int, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with name {match_id} not found")
    # check if the current user is the home team manager
    home_team = get_team(match.home_team_name)
    home_team_manager = get_team_manager(home_team)
    if home_team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {home_team_manager} manager")
    requests = get_match_teams_requests(match)
    if not requests:
        raise HTTPException(
            status_code=404, detail=f"No team requests for match {match_id} found")
    return requests


# update team request to join my match
@managers_router.put("/update_team_request/{team_name}/{match_id}/{is_accepted}", response_model=TeamMatchRequest)
async def update_team_request(team_name: str, match_id: str, is_accepted: bool, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with name {match_id} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with username {team_name} not found")
    # check if the current user is the home team manager
    home_team = get_team(match.home_team_name)
    home_team_manager = get_team_manager(home_team)
    if home_team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {home_team_manager} manager")
    # check if team request exists
    team_request = get_match_team_request(team, match)
    if not team_request:
        raise HTTPException(
            status_code=404, detail=f"Team request for {team_name} not found")
    # if is_accepted is true, check if the away team is already assigned to the match
    if is_accepted == True:
        away_team = get_match_team(match, team)
        if away_team:
            raise HTTPException(
                status_code=400, detail=f"Away team {away_team.team_name} is already assigned to the {match.match_id} match")
        # set away team to the team
        match.away_team_name = team.team_name
        # update match away
        update_match(match)
        add_match_team(match, team, is_home_team=False)
    # update team Match Request
    request_approval = TeamMatchRequest(
        team_request.match_id, team_request.team_id, is_accepted=is_accepted)
    return update_match_team_request(request_approval)


# remove team from my match
@managers_router.delete("/remove_my_match_team/{team_name}/{match_id}")
async def remove_my_match_team(team_name: str, match_id: int, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"{team_name} has no team profile")
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with id: {match_id} not found")
    # get match team
    match_team = get_match_team(match, team)
    if not match_team:
        raise HTTPException(
            status_code=404, detail=f"Team {team_name} is not assigned to match {match_id}")
    # check if the current user is the home team manager
    home_team = get_team(match.home_team_name)
    home_team_manager = get_team_manager(home_team)
    if home_team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"User {current_user.username} is not {home_team_manager} manager")
    # update match away team to null
    match.away_team_name = None
    # update match
    update_match(match)
    return remove_match_team(match, team)


# add the away team to a match
@managers_router.put("/add_away_team/{match_id}/{team_name}", response_model=MatchTeamLink)
async def add_away_team(match_id: int, team_name: str, current_user: User = Security(get_current_active_user, scopes=["managers"])):
    # check if match exists
    match = get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=404, detail=f"Match with match id {match_id} not found")
    # check if current user is the home team manager
    home_team = match.home_team_name
    team_manager = get_team_manager(get_team(home_team))
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"Current user is not the home team manager")
    # check if away team exists
    away_team = get_team(team_name)
    if not away_team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name {team_name} not found")
    # check if home team is not the away team
    if match.home_team_id == away_team.team_id:
        raise HTTPException(
            status_code=404, detail=f"Match with match id {match_id} is already full")
    return assign_match_away_team(match, away_team)
