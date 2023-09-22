from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_admin, get_coach, get_coach_stadiums
from ..models import User, StadiumCoachLink
from typing import List


####################################  Stadium Coaches Section  ############################################################################################################
stadium_coaches_router = APIRouter(prefix="/stadium_coaches",
                                   tags=["Stadium Coaches"],
                                   dependencies=[Depends(oauth2_scheme)],
                                   responses={404: {"description": "Stadium Coaches Not found"}},)


# get coach's stadiums
@stadium_coaches_router.get("/get_coach_stadiums/{coach_username}", response_model=List[StadiumCoachLink])
async def read_coach_stadiums(coach_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} not found")
    stadiums = get_coach_stadiums(coach)
    if not stadiums:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} has no stadiums")
    return stadiums
