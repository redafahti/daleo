from fastapi import APIRouter, Depends, HTTPException, Security
from ..dependencies import oauth2_scheme, get_current_active_user, get_current_location, get_user, create_coach, get_coach, update_coach, update_coach_rating, get_player, get_coach_players, delete_coach, get_coach_players_requests, get_coach_player_request, update_coach_player_request, get_coaches_in_radius, get_stadium, get_coaches_by_stadium, get_coaches_by_rating
from ..models import CoachCreate, CoachRead, CoachUpdate, User, PlayerCoachRequest, PlayerRead
from typing import List


######################################  Coaches Section  ############################################################################################################
coaches_router = APIRouter(prefix="/coaches",
                           tags=["Coaches"],
                           dependencies=[Depends(oauth2_scheme)],
                           responses={404: {"description": "Coach Not found"}},)


# coaches root
@coaches_router.get("/")
async def read_root(current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    return{"Welcome to Team Up Coaches Section"}


# create my coach profile
@coaches_router.post("/create_coach/me", response_model=CoachRead)
async def create_my_coach_profile(coach_player_hourly_rate: int | None = None, coach_team_hourly_rate: int | None = None, current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if user exists
    user = get_user(current_user.username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username: {current_user.username} not found")
    # check if coach already exists
    if user.coach_id:
        raise HTTPException(
            status_code=404, detail=f"User with username: {current_user.username} already has a coach profile")
    # get coach current location
    coach_latitude, coach_longitude  = get_current_location()
    # check if coach has all the required fields
    new_coach = CoachCreate(username=current_user.username, coach_player_hourly_rate=coach_player_hourly_rate, coach_team_hourly_rate=coach_team_hourly_rate, coach_longitude=coach_longitude,
                            coach_latitude=coach_latitude, total_rating_count=0.0, total_rating=0, user_id=user.id)
    # create coach
    return create_coach(new_coach)


# get my coach profile
@coaches_router.get("/get_coach/me", response_model=CoachRead)
async def get_my_coach_profile(current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if coach exists
    coach = get_coach(current_user.username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {current_user.username} not found")
    return coach


# update my coach profile
@coaches_router.put("/update_coach/me", response_model=CoachRead)
async def update_my_coach_profile(coach_hourly_rate: int | None = None, current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if current user is a coach
    coach = get_coach(current_user.username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"User: {current_user.username} has no coach profile")
    # check if coach fields are valid
    coach_update = CoachUpdate(coach_hourly_rate=coach_hourly_rate)
    return update_coach(coach_update)


# update my geo location
@coaches_router.put("/update_coach_location/me", response_model=CoachRead)
async def update_my_location(current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if coach exists
    coach = get_coach(current_user.username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {current_user.username} not found")
    # get coach current location
    coach_latitude, coach_longitude  = get_current_location()
    coach_update = CoachUpdate(username=current_user.username,
                               coach_latitude=coach_latitude, coach_longitude=coach_longitude)
    return update_coach(coach_update)


# get my rating count and rating
@coaches_router.get("/get_coach_rating/me")
async def get_my_coach_rating(current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if coach exists
    coach = get_coach(current_user.username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {current_user.username} not found")
    # update coach's ratings
    updated_coach = update_coach_rating(coach)
    if not updated_coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {current_user.username} has no ratings")
    return {updated_coach.total_rating_count, updated_coach.total_rating}


# get my players
@coaches_router.get("/get_coach_players/me", response_model=List[PlayerRead])
async def get_my_players(current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if current user is a coach
    coach = get_coach(current_user.username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {current_user.username} not found")
    players = get_coach_players(coach)
    if not players:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {current_user.username} has no players")
    return players


# get my players coach requests
@coaches_router.get("/get_coach_players_requests/me", response_model=List[PlayerCoachRequest])
async def get_my_players_coach_requests(current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if current user is a coach
    coach = get_coach(current_user.username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {current_user.username} not found")
    requests = get_coach_players_requests(coach)
    if not requests:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {current_user.username} has no requests")
    return requests


# update my player coach request
@coaches_router.put("/update_player_coach_request/{player_username}", response_model=PlayerCoachRequest)
async def update_my_player_coach_request(player_username: str, is_accepted: bool, current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if current user is a coach
    coach = get_coach(current_user.username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {current_user.username} not found")
    # check if player exists
    player = get_player(player_username)
    if not player:
        raise HTTPException(
            status_code=404, detail=f"Player with username {player_username} not found")
    # check if request exists
    coach_request = get_coach_player_request(player, coach)
    if not coach_request:
        raise HTTPException(
            status_code=404, detail=f"Player with username {player_username} has no request")
    # update request
    request_update = PlayerCoachRequest(
        request_id=coach_request.request_id, player_id=player.player_id, coach_id=coach.coach_id, is_accepted=is_accepted)
    return update_coach_player_request(request_update)


# delete coach
@coaches_router.delete("/delete_coach/me")
async def delete_my_coach_profile(current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # Check if coach exists
    coach = get_coach(current_user.username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"User: {current_user.username} has no coach profile")
    # delete coach
    return delete_coach(coach)


########################################### Coach Access Section ######################################################################
# get coach
@coaches_router.get("/get_coach/{coach_username}", response_model=CoachRead)
async def get_coach_profile(coach_username: str, current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} not found")
    return coach


# get coach's rating count and rating
@coaches_router.get("/get_coach_rating/{coach_username}")
async def get_coach_rating(coach_username: str, current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} not found")
    # update coach's ratings
    updated_coach = update_coach_rating(coach)
    if not updated_coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} has no ratings")
    return {updated_coach.total_rating_count, updated_coach.total_rating}


# find coaches by location
@coaches_router.get("/find_coaches_by_location/{radius}", response_model=List[CoachRead])
async def find_coaches_by_location(radius: float, current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # get user current location
    user_latitude, user_longitude  = get_current_location()
    coaches = get_coaches_in_radius(
        longitude=user_longitude, latitude=user_latitude, radius=radius)
    if not coaches:
        raise HTTPException(
            status_code=404, detail=f"No coaches found in radius {radius}")
    return coaches


# find coaches by home stadium
@coaches_router.get("/find_coaches_by_stadium/{stadium_id}", response_model=List[CoachRead])
async def find_coaches_by_stadium(stadium_id: int, current_user: User = Security(get_current_active_user, scopes=["coaches"])):
    # check if stadium exists
    stadium = get_stadium(stadium_id)
    if not stadium:
        raise HTTPException(
            status_code=404, detail=f"Stadium with id: {stadium_id} not found")
    coaches = get_coaches_by_stadium(stadium)
    if not coaches:
        raise HTTPException(
            status_code=404, detail=f"No coaches found in stadium with id: {stadium_id}")
    return coaches


# find coaches by rating
@coaches_router.get("/find_coaches_by_rating/{rating}", response_model=List[CoachRead])
async def find_coaches_by_rating(rating: float):
    coaches = get_coaches_by_rating(rating)
    if not coaches:
        raise HTTPException(
            status_code=404, detail=f"No coaches found with rating: {rating}")
    return coaches
