from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_admin, get_referee, get_referee_stadiums
from ..models import User, StadiumRefereeLink
from typing import List


####################################  Stadium Referees Section  ############################################################################################################
stadium_referees_router = APIRouter(prefix="/stadium_referees",
                                    tags=["Stadium Referees"],
                                    dependencies=[Depends(oauth2_scheme)],
                                    responses={404: {"description": "Stadium referees Not found"}},)


# get referee's stadiums
@stadium_referees_router.get("/get_referee_stadiums/{referee_username}", response_model=List[StadiumRefereeLink])
async def read_referee_stadiums(referee_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if referee exists
    referee = get_referee(referee_username)
    if not referee:
        raise HTTPException(
            status_code=404, detail=f"Referee with username {referee_username} not found")
    stadiums = get_referee_stadiums(referee)
