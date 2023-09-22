from fastapi import APIRouter, Depends, Security
from ..dependencies import oauth2_scheme, get_current_location, get_current_active_user, get_stadiums_within_radius, get_stadiums_by_city, get_stadium, get_stadium_teams, get_stadium_team, get_team
from ..models import StadiumRead, User, TeamRead
from typing import List
from fastapi import HTTPException


####################################  Stadiums Main Section ###############################################################################
stadiums_router = APIRouter(prefix="/stadiums",
                            tags=["Stadiums"],
                            dependencies=[Depends(oauth2_scheme)],
                            responses={404: {"description": "Stadium Not found"}},)


# get stadiums within radius
@stadiums_router.get("/get_stadiums_within_radius/{radius}", response_model=List[StadiumRead])
async def find_stadiums_within_radius(radius: int, current_user: User = Security(get_current_active_user, scopes=["stadiums"])):
    latitude, longitude = get_current_location()
    stadiums = get_stadiums_within_radius(
        longitude=longitude, latitude=latitude, radius=radius)
    if not stadiums:
        raise HTTPException(status_code=404, detail="Stadiums not found")
    return stadiums


# get stadium by city
@stadiums_router.get("/get_stadiums_by_city/{stadium_city}", response_model=List[StadiumRead])
async def find_stadiums_by_city(stadium_city: str, current_user: User = Security(get_current_active_user, scopes=["stadiums"])):
    stadiums = get_stadiums_by_city(stadium_city)
    if not stadiums:
        raise HTTPException(status_code=404, detail="Stadiums not found")
    return stadiums


# get stadium teams
@stadiums_router.get("/get_stadium_teams/{stadium_id}", response_model=List[TeamRead])
async def find_stadium_teams(stadium_id: int, current_user: User = Security(get_current_active_user, scopes=["stadiums"])):
    # check if stadium exists
    stadium = get_stadium(stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    teams = get_stadium_teams(stadium_id)
    if not teams:
        raise HTTPException(status_code=404, detail="Stadium has no teams")
    return teams


# get stadium team
@stadiums_router.get("/get_stadium_team/{stadium_id}/{team_id}", response_model=TeamRead)
async def find_stadium_team(stadium_id: int, team_id: int, current_user: User = Security(get_current_active_user, scopes=["stadiums"])):
    # check if stadium exists
    stadium = get_stadium(stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    # check if team exists
    team = get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    # check if team is in the stadium
    stadium_team = get_stadium_team(stadium_id, team_id)
    if not stadium_team:
        raise HTTPException(status_code=404, detail="Team not in stadium")
    return stadium_team
