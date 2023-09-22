from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_user, get_current_active_admin, all_coaches, create_coach, get_coach, get_coaches_in_radius, get_coaches_by_rating, update_coach, delete_coach
from ..models import User, CoachRead, CoachCreate, CoachUpdate
from typing import List

####################################  Coaches Admin Section  ############################################################################################################
coaches_admin_router = APIRouter(prefix="/coaches_admin",
                                 tags=["Coaches Admin"],
                                 dependencies=[Depends(oauth2_scheme)],
                                 responses={404: {"description": "Coach Not found"}},)


# get all coaches
@coaches_admin_router.get("/get_coaches", response_model=List[CoachRead])
async def get_all_coaches(current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return all_coaches()


# create coach
@coaches_admin_router.post("/create_coach/{username}", response_model=CoachRead)
async def create_new_coach(username: str, coach_player_hourly_rate: int | None = None, coach_team_hourly_rate: int | None = None, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if user exists
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username: {username} not found")
    # check if coach already exists
    if user.coach_id:
        raise HTTPException(
            status_code=404, detail=f"User with username: {username} already has a coach profile")
    # check if coach has all the required fields
    new_coach = CoachCreate(username=username, coach_player_hourly_rate=coach_player_hourly_rate,
                            coach_team_hourly_rate=coach_team_hourly_rate, user_id=user.id)
    return create_coach(new_coach)


# get coach
@coaches_admin_router.get("/get_coach/{coach_username}", response_model=CoachRead)
async def get_coach_profile(coach_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} not found")
    return coach


# find coaches by location radius
@coaches_admin_router.get("/find_coaches_by_location/{longitude}/{latitude}/{radius}", response_model=List[CoachRead])
async def find_coaches_in_radius(longitude: float, latitude: float, radius: float, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    coaches = get_coaches_in_radius(
        longitude=longitude, latitude=latitude, radius=radius)
    if not coaches:
        raise HTTPException(
            status_code=404, detail=f"No coaches found in the radius")
    return coaches


# get coach's rating count and rating
@coaches_admin_router.get("/get_coach_rating/{coach_username}")
async def get_coach_rating(coach_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
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


# get coaches by rating
@coaches_admin_router.get("/get_coaches_by_rating/{rating}", response_model=List[CoachRead])
async def find_coaches_by_rating(rating: int, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    coaches = get_coaches_by_rating(rating)
    if not coaches:
        raise HTTPException(
            status_code=404, detail=f"No coaches found with rating: {rating}")
    return coaches


# update coach
@coaches_admin_router.put("/update_coach/{coach_username}", response_model=CoachRead)
async def update_coach_profile(coach_username: str, coach_player_hourly_rate: int | None = None, coach_team_hourly_rate: int | None = None, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"User: {coach_username} has no coach profile")
    # check if coach fields are valid
    coach_update = CoachUpdate(username=coach_username, coach_player_hourly_rate=coach_player_hourly_rate,
                               coach_team_hourly_rate=coach_team_hourly_rate)
    return update_coach(coach_update)


# update coach rating
@coaches_admin_router.put("/update_coach_rating/{coach_username}", response_model=CoachRead)
async def update_coach_rating(coach_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"User: {coach_username} has no coach profile")
    # update coach's ratings
    return update_coach_rating(coach)


# delete coach
@coaches_admin_router.delete("/delete_coach/{coach_username}")
async def delete_coach_profile(coach_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # Check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"User: {coach_username} has no coach profile")
    # delete coach
    return delete_coach(coach)
