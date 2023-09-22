from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_user, get_user, get_team, get_team_manager, get_stadium, get_stadium_available_pitches, create_match, add_match_team, get_match_team_requests, get_team_player_request, update_team_player_request, get_player, create_player, update_team, create_team, delete_team
from ..models import User, MatchTeamLink, MatchCreate, TeamMatchRequest, PlayerTeamRequest, TeamPlayerLink, PlayerCreate, TeamUpdate
from datetime import datetime
from typing import List


############################# Match Manager Section #####################################################################################################
match_manager_router = APIRouter(prefix="/match_manager",
                                 tags=["Match Manager"],
                                 dependencies=[Depends(oauth2_scheme)],
                                 responses={404: {"description": "Match Managers Not found"}},)


# create a match
@match_manager_router.post("/create_match", response_model=MatchTeamLink)
async def new_match(team_name: str, stadium_id: int, match_duration: int, match_start_time: datetime, teams_size: int, number_of_substitutes: int | None = None, match_type: str | None = None, match_prize: int | None = None, current_user: User = Security(get_current_active_user, scopes=["matches"])):
    # check if team exists
    home_team = get_team(team_name)
    if not home_team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name {team_name} not found")
    # check if current user is the team manager
    team_manager = get_team_manager(home_team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"Current user is not the team manager")
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
    match_team = add_match_team(match, home_team, is_home_team=True)
    return match_team


# get team request to join match
@match_manager_router.get("/get_team_requests/{team_name}", response_model=List[TeamMatchRequest])
async def read_team_requests(team_name: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"Current user is not the team manager")
    return get_match_team_requests(team)


# update player request to join team
@match_manager_router.put("/update_player_request/{player_username}/{team_name}/{is_accepted}", response_model=PlayerTeamRequest)
async def update_player_request(player_username: str, team_name: str, is_accepted: bool, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if current user is the team manager
    team_manager = get_team_manager(get_team(team_name))
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"Current user is not the team manager")
    # check if player request exists
    player_request = get_team_player_request(player_username, team_name)
    if not player_request:
        raise HTTPException(
            status_code=404, detail=f"Player request for {player_username} not found")
    # approve player Team Request
    request_approval = PlayerTeamRequest(
        player_request.team_id, player_request.player_id, is_accepted=is_accepted)
    return update_team_player_request(request_approval)


# Add team
@match_manager_router.post("/add_team/{player_username}", response_model=TeamPlayerLink)
async def assign_player_to_team(player_username: str, team_name: str, is_captain: bool | None = False, player_position: str | None = None, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if player exists and create player if not
    player = get_player(player_username)
    if not player:
        user = get_user(player_username)
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with username: {player_username} not found")
        new_player = PlayerCreate(username=user.username, user_id=user.id)
        player = create_player(new_player)
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team named: {team_name} not found")
    # check if current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"Current user is not the team manager")
    # check if player is already assigned to the team
    team = get_team(player, team)
    if team:
        raise HTTPException(
            status_code=404, detail=f"Player with username: {player_username} is already assigned to the {team_name} team")
    if not team:
        # check if team has request
        team_request = get_team_player_request(team, player)
        # if team has request update it
        if team_request:
            team_request.is_accepted = True
            update_team_player_request(team_request)
        new_team = TeamPlayerLink(
            player_id=player.player_id, team_id=team.team_id, is_captain=is_captain, player_position=player_position)
    # update team captain if player is assigned as captain
    if is_captain == True:
        captain_update = TeamUpdate(
            team_name=team.team_name, captain_id=player.player_id)
        update_team(captain_update)
    return create_team(new_team)


# remove team
@match_manager_router.put("/remove_team/{team_name}")
async def remove_team(team_name: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail=f"Current user is not the team manager")
    return delete_team(team)
