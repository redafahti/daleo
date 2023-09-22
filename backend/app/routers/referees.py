from fastapi import APIRouter, Depends, HTTPException, Security
from ..dependencies import oauth2_scheme, get_current_active_user, get_current_location, get_user, get_referee, create_referee, get_referees_in_radius, update_referee_rating, get_referees_by_rating, update_referee, delete_referee
from ..models import Referee, RefereeRead, User, RefereeUpdate
from typing import List


##################### Referees Main Section ############################################################################################################
referees_router = APIRouter(prefix="/referees",
                            tags=["Referees"],
                            dependencies=[Depends(oauth2_scheme)],
                            responses={404: {"description": "Referee Not found"}},)


# referees root
@referees_router.get("/")
async def read_root(current_user: User = Security(get_current_active_user, scopes=["referees"])):
    return{"Welcome to Team Up referees Section"}


# create my referee profile
@referees_router.post("/create_referee_profile/me", response_model=RefereeRead)
async def create_my_referee_profile(current_user: User = Security(get_current_active_user, scopes=["referees"])):
    # check if user exists
    user = get_user(current_user.username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username: {current_user.username} not found")
    # check if referee already exists
    if user.referee_id:
        raise HTTPException(
            status_code=404, detail=f"User with username: {current_user.username} already has a referee profile")
    # check if referee has all the required fields
    new_referee = Referee(username=current_user.username, user_id=user.id)
    return create_referee(new_referee)


# get my referee profile
@referees_router.get("/get_referee_profile/me", response_model=RefereeRead)
async def get_my_referee_profile(username: str, current_user: User = Security(get_current_active_user, scopes=["referees"])):
    referee = get_referee(username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username {username} not found")
    return referee


# update my referee profile
@referees_router.put("/update_referee_profile/me", response_model=RefereeRead)
async def update_my_referee_profile(username: str, referee_rating: int | None = None, current_user: User = Security(get_current_active_user, scopes=["referees"])):
    referee = get_referee(username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username {username} not found")
    referee_update = RefereeUpdate(
        username=username, referee_rating=referee_rating)
    return update_referee(referee_update)


# update my geo location
@referees_router.put("/update_referee_location/me", response_model=RefereeRead)
async def update_my_location(current_user: User = Security(get_current_active_user, scopes=["referees"])):
    # check if referee exists
    referee = get_referee(current_user.username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username: {current_user.username} not found")
    # get referee current location
    referee_latitude, referee_longitude = get_current_location()
    referee_update = RefereeUpdate(username=current_user.username,
                                   referee_latitude=referee_latitude, referee_longitude=referee_longitude)
    return update_referee(referee_update)


# get my rating count and rating
@referees_router.get("/get_referee_rating/me")
async def get_my_referee_rating(current_user: User = Security(get_current_active_user, scopes=["referees"])):
    # check if referee exists
    referee = get_referee(current_user.username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username: {current_user.username} not found")
    # update referee's ratings
    updated_referee = update_referee_rating(referee)
    if not updated_referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username: {current_user.username} has no ratings")
    return {updated_referee.total_rating_count, updated_referee.total_rating}


# delete referee
@referees_router.delete("/delete_referee_profile/me")
async def delete_my_refree_profile(username: str, current_user: User = Security(get_current_active_user, scopes=["referees"])):
    referee = get_referee(username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username {username} not found")
    return delete_referee(referee)


# find referees in my location radius
@referees_router.get("/find_referees_by_radius/{radius}", response_model=List[RefereeRead])
async def find_referees_in_my_radius(radius: float, current_user: User = Security(get_current_active_user, scopes=["referees"])):
    # check if referee exists
    referee = get_referee(current_user.username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username: {current_user.username} not found")
    # get referee current location
    referee_latitude, referee_longitude = get_current_location()
    referee_update = RefereeUpdate(username=current_user.username,
                                   referee_latitude=referee_latitude, referee_longitude=referee_longitude)
    updated_referee = update_referee(referee_update)
    return get_referees_in_radius(longitude=updated_referee.referee_longitude, latitude=updated_referee.referee_latitude, radius=radius)


# find referees by rating and my location radius
@referees_router.get("/find_referees_by_rating_radius", response_model=List[RefereeRead])
async def find_referees_by_rating_in_my_radius(rating: int, radius: float, current_user: User = Security(get_current_active_user, scopes=["referees"])):
    # check if referee exists
    referee = get_referee(current_user.username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username: {current_user.username} not found")
    # get referee current location
    referee_latitude, referee_longitude = get_current_location()
    referee_update = RefereeUpdate(username=current_user.username,
                                   referee_latitude=referee_latitude, referee_longitude=referee_longitude)
    updated_referee = update_referee(referee_update)
    return get_referees_by_rating(referee=updated_referee, rating=rating, radius=radius)
