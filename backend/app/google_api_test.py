import googlemaps
from googlemaps.exceptions import ApiError
from dotenv import load_dotenv
import os
load_dotenv()

# Google Maps API
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

# get stadium by city from Google Places API


def get_google_city_stadiums(city: str):
    try:
        response = gmaps.places(
            query=f"terrains de proximité de football in {city}", type="football stadium")
        stadiums = response["results"]
        return stadiums
    except ApiError as e:
        return {"error": str(e)}


#stadiums = get_google_city_stadiums("Casablanca")
# print(stadiums)


# get stadium image
def get_stadium_image(reference_id: str, maxwidth: int, maxheight: int, ):

    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&maxheight=400&photo_reference={reference_id}&key={os.getenv('GOOGLE_MAPS_API_KEY')}"


stadium_photo = get_stadium_image(reference_id='AUacShjRM3V1bcepJsStk2N72LDXirsF_l1WistUgV9cp-Nn14VPgr59D3U08te_9ix29_Q56DskwOx7sw-fsHANBg2FpfNx-_z6QCrm1152MjgUf9P9ZS53R4dTv2hkPK-pcDsnDJB1icWyR_D1v_cuEGIMS_BIR1wo56jsspl9jTujp2c8',
                                  maxwidth=400,  maxheight=400)

print(stadium_photo)
