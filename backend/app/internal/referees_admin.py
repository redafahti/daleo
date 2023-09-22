from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_user, get_current_active_admin, all_referees, create_referee, get_referee, get_referees_in_radius, get_referees_by_rating, update_referee, delete_referee
from ..models import User, RefereeRead, Referee, RefereeUpdate
from typing import List


##################### Referees Admin Section ############################################################################################################
referees_admin_router = APIRouter(prefix="/referees_admin",
                                  tags=["Referees Admin"],
                                  dependencies=[Depends(oauth2_scheme)],
                                  responses={404: {"description": "Referee Admin Not found"}},)


# get all referees
@referees_admin_router.get("/get_referees", response_model=List[RefereeRead])
async def get_all_referees(current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return all_referees()


# create referee
@referees_admin_router.post("/create_referee/{username}", response_model=RefereeRead)
async def create_new_referee(username: str, referee_hourly_rate: int | None = None, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if user exists
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username: {username} not found")
    # check if referee already exists
    if user.referee_id:
        raise HTTPException(
            status_code=404, detail=f"User with username: {username} already has a referee profile")
    # check if referee has all the required fields
    new_referee = Referee(
        username=username, referee_hourly_rate=referee_hourly_rate, user_id=user.id)
    return create_referee(new_referee)


# get referee
@referees_admin_router.get("/get_referee/{referee_username}", response_model=RefereeRead)
async def get_referee_profile(referee_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    referee = get_referee(referee_username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username {referee_username} not found")
    return referee


# find referees by location radius
@referees_admin_router.get("/find_referees_by_location/{longitude}/{latitude}/{radius}", response_model=List[RefereeRead])
async def find_referees_in_radius(longitude: float, latitude: float, radius: float, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return get_referees_in_radius(longitude=longitude, latitude=latitude, radius=radius)


# get referee's rating count and rating
@referees_admin_router.get("/get_referee_rating/{referee_username}")
async def get_referee_rating(referee_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if referee exists
    referee = get_referee(referee_username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username: {referee_username} not found")
    # update referee's ratings
    updated_referee = update_referee_rating(referee)
    if not updated_referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username: {referee_username} has no ratings")
    return {updated_referee.total_rating_count, updated_referee.total_rating}


# get referees by rating
@referees_admin_router.get("/get_referees_by_rating/{rating}", response_model=List[RefereeRead])
async def find_referees_by_rating(rating: int, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return get_referees_by_rating(rating)


# update referee
@referees_admin_router.put("/update_referee/{referee_username}", response_model=RefereeRead)
async def update_referee_profile(referee_username: str, referee_hourly_rate: int | None = None, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    referee = get_referee(referee_username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username {referee_username} not found")
    referee_update = RefereeUpdate(
        username=referee_username, referee_rating=referee_hourly_rate)
    return update_referee(referee_update)


# update referee rating
@referees_admin_router.put("/update_referee_rating/{referee_username}", response_model=RefereeRead)
async def update_referee_rating(referee_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if referee exists
    referee = get_referee(referee_username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"User: {referee_username} has no referee profile")
    # update referee's ratings
    return update_referee_rating(referee)


# delete referee
@referees_admin_router.delete("/delete_referee/{username}")
async def delete_referee_profile(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    referee = get_referee(username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username {username} not found")
    return delete_referee(referee)
