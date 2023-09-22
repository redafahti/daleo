from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_user, get_current_active_admin, all_stadiums, get_stadium, create_stadium, update_stadium, get_google_city_stadiums, get_stadium_by_place_id, format_stadium_info, delete_stadium
from ..models import User, StadiumRead, StadiumCreate, Stadium, StadiumUpdate
from typing import List
from pydantic import EmailStr
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()


####################################  Stadium Admin Section ###############################################################################
stadiums_admin_router = APIRouter(prefix="/stadiums_admin",
                                  tags=["Stadiums Admin"],
                                  dependencies=[Depends(oauth2_scheme)],
                                  responses={404: {"description": "stadium Not found"}},)


# stadiums root
@stadiums_admin_router.get("/")
async def read_root(current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return{"Welcome to Team Up Stadiums Admin Section"}


# get all stadiums in database
@stadiums_admin_router.get("/get_all_stadiums", response_model=List[StadiumRead])
async def get_all_stadiums(current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    stadiums = all_stadiums()
    if not stadiums:
        raise HTTPException(status_code=404, detail="Stadiums not found")
    return stadiums


# add a new stadium
@stadiums_admin_router.post("/create_stadium/{stadium_name}", response_model=StadiumRead)
async def new_stadium(
        stadium_name: str,
        number_of_pitches: int | None = 1,
        stadium_image_url: str | None = None,
        stadium_contact_name: str | None = None,
        stadium_email: EmailStr | None = None,
        stadium_phone_number: str | None = None,
        stadium_website: str | None = None,
        stadium_address: str | None = None,
        stadium_longitude: float | None = None,
        stadium_latitude: float | None = None,
        stadium_neighborhood: str | None = None,
        stadium_city: str | None = None,
        stadium_opening_time: datetime | None = None,
        stadium_closing_time: datetime | None = None,
        stadium_open_now: bool | None = None,
        stadium_rating_total: int | None = 0,
        stadium_rating: float | None = 0.0,
        google_place_id: str | None = None,
        stadium_manager_id: int | None = None,
        current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    if stadium_manager_id:
        stadium_manager_id = get_user(stadium_manager_id)
        if not stadium_manager_id:
            raise HTTPException(
                status_code=404, detail="Stadium manager user account not found")
    stadium_manager_id = current_admin.id
    new_stadium = StadiumCreate(
        stadium_name=stadium_name,
        number_of_pitches=number_of_pitches,
        stadium_image_url=stadium_image_url,
        stadium_contact_name=stadium_contact_name,
        stadium_email=stadium_email,
        stadium_phone_number=stadium_phone_number,
        stadium_website=stadium_website,
        stadium_address=stadium_address,
        stadium_longitude=stadium_longitude,
        stadium_latitude=stadium_latitude,
        stadium_neighborhood=stadium_neighborhood,
        stadium_city=stadium_city,
        stadium_opening_time=stadium_opening_time,
        stadium_closing_time=stadium_closing_time,
        stadium_open_now=stadium_open_now,
        stadium_rating_total=stadium_rating_total,
        stadium_rating=stadium_rating,
        google_place_id=google_place_id,
        stadium_manager_id=stadium_manager_id
    )
    return create_stadium(new_stadium)


# update stadium
@stadiums_admin_router.put("/update_stadium/{stadium_id}", response_model=StadiumRead)
async def stadium_update(
    stadium_id: int,
    stadium_name: str | None = None,
    number_of_pitches: int | None = 1,
    stadium_image_url: str | None = None,
    stadium_contact_name: str | None = None,
    stadium_email: EmailStr | None = None,
    stadium_phone_number: str | None = None,
    stadium_website: str | None = None,
    stadium_address: str | None = None,
    stadium_longitude: float | None = None,
    stadium_latitude: float | None = None,
    stadium_neighborhood: str | None = None,
    stadium_city: str | None = None,
    stadium_opening_time: datetime | None = None,
    stadium_closing_time: datetime | None = None,
    stadium_open_now: bool | None = None,
    stadium_rating_total: int | None = 0,
    stadium_rating: float | None = 0.0,
    google_place_id: str | None = None,
    stadium_manager_id: int | None = None,
    current_admin: User = Security(get_current_active_admin, scopes=["admin"])
):
    stadium = get_stadium(stadium_id)
    if not stadium:
        raise HTTPException(
            status_code=404, detail=f"stadium with stadium name {stadium_id} not found")
    if stadium_manager_id:
        stadium_manager_id = get_user(stadium_manager_id)
        if not stadium_manager_id:
            raise HTTPException(
                status_code=404, detail="Stadium manager user account not found")
    stadium_manager_id = stadium.stadium_manager_id
    stadium_update = StadiumUpdate(
        stadium_name=stadium_name,
        number_of_pitches=number_of_pitches,
        stadium_image_url=stadium_image_url,
        stadium_contact_name=stadium_contact_name,
        stadium_email=stadium_email,
        stadium_phone_number=stadium_phone_number,
        stadium_website=stadium_website,
        stadium_address=stadium_address,
        stadium_longitude=stadium_longitude,
        stadium_latitude=stadium_latitude,
        stadium_neighborhood=stadium_neighborhood,
        stadium_city=stadium_city,
        stadium_opening_time=stadium_opening_time,
        stadium_closing_time=stadium_closing_time,
        stadium_open_now=stadium_open_now,
        stadium_rating_total=stadium_rating_total,
        stadium_rating=stadium_rating,
        google_place_id=google_place_id,
        stadium_manager_id=stadium_manager_id
    )
    # update stadium
    return update_stadium(stadium, stadium_update)


# Add stadiums from Google Places API to database if they don't already exist
@stadiums_admin_router.post("/add_google_city_stadiums/{city}", response_model=List[Stadium])
async def add_stadiums_from_google_by_city(city: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # get stadiums from Google Places API
    stadiums = get_google_city_stadiums(city)
    added_stadiums = []
    # iterate through stadiums
    for stadium in stadiums:
        # check if stadium already exists
        stadium_db = get_stadium_by_place_id(stadium['place_id'])
        if stadium_db:
            print(f"stadium with place_id {stadium['name']} already exists")
        else:
            # format stadium data
            formatted_stadium = format_stadium_info(stadium)
            # check if the stadium has all the required data
            if not formatted_stadium:
                print(
                    f"stadium with place_id {stadium['place_id']} does not have all the required data")
            else:
                new_stadium = StadiumCreate(**formatted_stadium)
                new_stadium.stadium_city = city
                new_stadium.stadium_manager_id = current_admin.id
                photo_reference = new_stadium.google_image_reference
                if photo_reference:
                    new_stadium.stadium_image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&maxheight=400&photo_reference={photo_reference}&key={os.getenv('GOOGLE_MAPS_API_KEY')}"
            new_stadium = create_stadium(new_stadium)
            added_stadiums.append(new_stadium)
    return added_stadiums


# delete stadium
@stadiums_admin_router.delete("/delete_stadium/{stadium_name}")
async def stadium_delete(stadium_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    stadium = get_stadium(stadium_name)
    if not stadium:
        raise HTTPException(
            status_code=404, detail=f"stadium with stadium name {stadium_name} not found")
    return delete_stadium(stadium_name)
