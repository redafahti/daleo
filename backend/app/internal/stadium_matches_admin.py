from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_admin, get_stadium_matches, get_stadium, get_all_matches_by_date
from ..models import User, MatchRead
from typing import List
from datetime import datetime, date


####################################  Stadium Matches Section ###############################################################################
stadium_matches_router = APIRouter(prefix="/stadium_matches",
                                   tags=["Stadium Matches"],
                                   dependencies=[Depends(oauth2_scheme)],
                                   responses={404: {"description": "Stadium match Not found"}},)


# get stadium matches
@stadium_matches_router.get("/get_stadium_matches/{stadium_name}", response_model=List[MatchRead])
async def find_stadium_matches(stadium_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return get_stadium_matches(stadium_name)


# get all matches by date range and stadium name
@stadium_matches_router.get("/get_stadium_matches_by_date/{stadium_name}/{start_date}/{end_date}", response_model=List[MatchRead])
async def get_stadium_matches_by_date(stadium_name: str, start_date: date, end_date: date, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if stadium exists
    stadium = get_stadium(stadium_name)
    if not stadium:
        raise HTTPException(
            status_code=404, detail=f"stadium with stadium name {stadium_name} not found")
    # check if start date is valid
    if start_date < datetime.now():
        raise HTTPException(
            status_code=404, detail=f"start date {start_date} is not valid")
    # check if end date is less than start date and valid
    if end_date < start_date:
        raise HTTPException(
            status_code=404, detail=f"end date {end_date} is before start date {start_date}")
    # get all matches in stadium by date range
    return get_all_matches_by_date(stadium_name, start_date, end_date)
