from fastapi import Depends, HTTPException, status, Security
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from datetime import datetime, timedelta, date
from .models import TokenData, User, EmailValidation, Manager, ManagerUpdate, ManagerCreate, Coach, CoachUpdate, StadiumCoachLink, StadiumRefereeLink, MatchCoachLink, Player, PlayerAvailability, PlayerUpdate, TeamUpdate, Referee, RefereeCreate, RefereeUpdate, Stadium, StadiumUpdate, Match, MatchCreate, Team, TeamPlayerLink, PlayerTeamInvitation, PlayerTeamRequest, PlayerMatchInvitation, PlayerMatchRequest, TeamMatchInvitation, TeamMatchRequest, MatchPlayerLink, MatchTeamLink, StadiumPlayerLink, StadiumTeamLink, TeamCoachLink, PlayerCoachLink, MatchScore, PlayerCoachRequest, TeamCoachRequest, TeamAvailability
from .database import PG_Engine
from pydantic import ValidationError
from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
import math
import random
import smtplib
from pydantic import EmailStr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import geocoder
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import googlemaps
from googlemaps.exceptions import ApiError
from dotenv import load_dotenv
import os
load_dotenv()


engine = PG_Engine()
base_url = os.getenv("BASE_URL")


############################################# Authentication Section #######################################################################
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "8c28a917d419607579317a73c29729811d6f1ccbf1b3ea6fd208fbc9fe331a0a"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "superuser": "Read information about superusers.",
        "admin": "Read information about admin users.",
        "users": "Read information about users.",
        "me": "Read information about the current user.",
        "managers": "Read information about managers.",
        "players": "Read information about players.",
        "invitations": "Read information about invitations.",
        "teams": "Read information about teams.",
        "stadiums": "Read information about stadiums.",
        "matches": "Read information about matches.",
        "referees": "Read information about referees.",
        "coaches": "Read information about coaches.",
    },
)

# Password Hasshing section


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# User Token section
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# User authentication section
def authenticate_user(username: str, password: str):
    user = get_user(username=username)
    if not user:
        raise HTTPException(
            status_code=401, detail=f"User with username {username} not found")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401, detail=f"Password incorrect for user with username {username}")
    return user


# get current user
async def get_current_user(
        security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


# get current active user
async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["me"])
):
    if current_user.disabled == True:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# get current active superuser
async def get_current_active_superuser(
    current_superuser: User = Security(get_current_user, scopes=["superuser"])
):
    if current_superuser.is_superuser == False:
        raise HTTPException(status_code=400, detail="User not superuser")
    return current_superuser


# get current active admin user
async def get_current_active_admin(
    current_admin: User = Security(
        get_current_user, scopes=["admin"])
):
    if current_admin.is_admin == False:
        raise HTTPException(status_code=400, detail="User not admin")
    return current_admin


########################################### locations section ##################################################################################
# Google Maps API
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))


def get_current_location():
    g = geocoder.ip('me')
    return g.latlng


def get_location(address: str):
    geolocator = Nominatim(user_agent="teamup")  # Initialize the geolocator
    # Pass an empty string to get the current location
    location = geolocator.geocode(address)

    if location is not None:
        return {"longitude": location.longitude, "latitude": location.latitude}
    else:
        raise HTTPException(
            status_code=404, detail=f"Failed to retrieve location.")


def get_address(latitude: float, longitude: float):
    geolocator = Nominatim(user_agent="teamup")  # Initialize the geolocator
    # Pass an empty string to get the current location
    location = geolocator.reverse(f"{latitude}, {longitude}")

    if location is not None:
        return {"address": location.address}
    else:
        raise HTTPException(
            status_code=404, detail=f"Failed to retrieve location.")


# get distance between two locations using geodesic distance
def get_distance(location1: dict, location2: dict):
    distance = geodesic((location1["latitude"], location1["longitude"]),
                        (location2["latitude"], location2["longitude"])).kilometers

    if distance is not None:
        return distance
    else:
        raise HTTPException(
            status_code=404, detail=f"Failed to retrieve distance.")


# Calculate the minimum and maximum latitude and longitude values based on the radius
def get_search_area(latitude: float, longitude: float, radius: int):
    min_longitude = longitude - radius / \
        abs(math.cos(math.radians(latitude)) * 111.0)
    max_longitude = longitude + radius / \
        abs(math.cos(math.radians(latitude)) * 111.0)
    min_latitude = latitude - (radius / 111.0)
    max_latitude = latitude + (radius / 111.0)
    return {"min_longitude": min_longitude, "max_longitude": max_longitude, "min_latitude": min_latitude, "max_latitude": max_latitude}

######################### email validation section ###########################################################################################
# Generate random 4 digits validation code


def generate_validation_code():
    return str(random.randint(1000, 9999))


# check if validation code is valid
def check_validation_code(email_validation: EmailValidation, validation_code: str):
    if email_validation.email_validation_code == validation_code and email_validation.email_validation_expiration > datetime.now():
        return True
    return False


# send email
def send_email(send_to: EmailStr, subject: str, html_message: str):
    smtp_username = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    send_from = os.getenv("EMAILS_FROM_EMAIL")

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = subject

    msg.attach(MIMEText(html_message, 'html'))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(send_from, send_to, msg.as_string())
        server.quit()  # Close the server connection after sending the email
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# create validation in database
def create_email_validation(user: User):
    with Session(engine) as session:
        try:
            validation = EmailValidation(
                email=user.email,
                user_id=user.id,
                email_validation_code=generate_validation_code(),
                email_validation_expiration=datetime.now() + timedelta(hours=24),
                send_from=os.getenv("SMTP_USER"),
                subject=f"{user.first_name}, Please validate your email address with Team Up"
            )
            db_validation = EmailValidation.from_orm(validation)
            session.add(db_validation)
            session.commit()
            session.refresh(db_validation)
            if not db_validation:
                raise HTTPException(
                    status_code=404, detail=f"Validation for {validation.email} not saved")
            return db_validation
        except Exception as e:
            session.rollback()
            raise e


# get validation from database
def get_email_validation(email: EmailStr):
    with Session(engine) as session:
        try:
            validation = session.exec(select(EmailValidation).where(
                EmailValidation.email == email)).first()
            if not validation:
                return None
            return validation
        except Exception as e:
            session.rollback()
            raise e


# Update validation in database
def update_email_validation(validation: EmailValidation):
    with Session(engine) as session:
        try:
            db_validation = EmailValidation.from_orm(validation)
            session.add(db_validation)
            session.commit()
            session.refresh(db_validation)
            if not db_validation:
                raise HTTPException(
                    status_code=404, detail=f"Validation for {validation.email} not saved")
            return db_validation
        except Exception as e:
            session.rollback()
            raise e


# delete validation in database
def delete_email_validation(validation: EmailValidation):
    with Session(engine) as session:
        try:
            db_validation = session.exec(select(EmailValidation).where(
                EmailValidation.email == validation.email)).first()
            session.delete(db_validation)
            session.commit()
            return {"message": f"Validation for {validation.email} deleted successfully"}
        except Exception as e:
            session.rollback()
            raise e


# send validation Email
def send_validation_email(validation: EmailValidation):
    subject = validation.subject
    send_to = validation.email
    validation_code = validation.email_validation_code

    link = f"{base_url}/validate_email/{send_to}/{validation_code}"

    html_message = f"""
            <html>
            <head></head>
            <body>
            <p>Please click on the following link to validate your email: <a href="{link}">{link}</a></p>
            </body>
            </html>
            """
    try:
        return send_email(send_to=send_to, subject=subject, html_message=html_message)
    except Exception as e:
        raise e


########################################################## User Section #######################################################################
# get all users
def get_users():
    with Session(engine) as session:
        return session.exec(select(User)).all()


# create user
def create_user(new_user: User):
    with Session(engine) as session:
        try:
            db_user = User.from_orm(new_user)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            if not db_user:
                raise HTTPException(
                    status_code=404, detail=f"User with username {new_user.username} not saved")
            return db_user
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"User with username {new_user.username} already exists")
        except Exception as e:
            session.rollback()
            raise e


# Update user
def update_user(user: User, user_update: User):
    with Session(engine) as session:
        try:
            user_dict = user_update.dict(exclude_unset=True)
            for key, value in user_dict.items():
                if value is not None:
                    setattr(user, key, value)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=404, detail=str(e))


# get user
def get_user(username: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(
            User.username == username)).first()
        if not user:
            return None
        return user


# get user by id
def get_user_by_id(user_id: int):
    with Session(engine) as session:
        user = session.exec(select(User).where(
            User.user_id == user_id)).first()
        if not user:
            return None
        return user


# get user by email
def get_user_by_email(email: EmailStr):
    with Session(engine) as session:
        user = session.exec(select(User).where(
            User.email == email)).first()
        if not user:
            return None
        return user


# Delete user
def delete_user(username: str):
    with Session(engine) as session:
        try:
            user = session.exec(select(User).where(
                User.username == username)).first()
            if not user:
                raise HTTPException(
                    status_code=404, detail=f"User with username {username} not found")
            session.delete(user)
            session.commit()
            return {"message": f"User with username {username} deleted"}
        except Exception as e:
            session.rollback()
            raise e


################################ Managers section ##################################################################################
# get all managers
def all_managers():
    with Session(engine) as session:
        return session.exec(select(Manager)).all()


# create manager
def create_manager(new_manager: ManagerCreate):
    with Session(engine) as session:
        try:
            db_manager = Manager.from_orm(new_manager)
            session.add(db_manager)
            session.commit()
            session.refresh(db_manager)
            if not db_manager:
                raise HTTPException(
                    status_code=404, detail=f"Manager with username {new_manager.username} not saved!")
            update_manager_id(db_manager.user_id, db_manager.manager_id)
            return db_manager
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Manager with username {new_manager.username} already exists")
        except Exception as e:
            session.rollback()
            raise e


# get manager
def get_manager(username: str):
    with Session(engine) as session:
        statement = select(Manager).where(Manager.username == username)
        manager = session.exec(statement).first()
        if not manager:
            return None
        return manager


# update manager
def update_manager(manager: ManagerUpdate):
    with Session(engine) as session:
        statement = select(Manager).where(
            Manager.username == manager.username)
        results = session.exec(statement)
        db_manager = results.first()
        if not db_manager:
            raise HTTPException(
                status_code=404, detail=f"Manager with username {manager.username} not found")
        manager_dict = manager.dict(exclude_unset=True)
        for key, value in manager_dict.items():
            if value is not None:
                setattr(db_manager, key, value)
        session.add(db_manager)
        session.commit()
        session.refresh(db_manager)

        return db_manager


# get all teams managers
def get_teams_managers():
    with Session(engine) as session:
        statement = select(Manager).where(Manager.manager_id != None)
        managers = session.exec(statement).all()
        if not managers:
            return None
        return managers

# get all manager teams


def get_manager_teams(manager: Manager):
    with Session(engine) as session:
        statement = select(Team).where(Team.manager_id == manager.manager_id)
        teams = session.exec(statement).all()
        if not teams:
            return None
        return teams


# get team's manager
def get_team_manager(team: Team):
    with Session(engine) as session:
        statement = select(Manager).where(
            Manager.manager_id == team.manager_id)
        manager = session.exec(statement).first()
        if not manager:
            return None
        return manager


# assign team manager
def assign_team_manager(manager: Manager, team: Team):
    with Session(engine) as session:
        try:
            team.manager_id = manager.manager_id
            session.add(team)
            session.commit()
            session.refresh(team)
            return team
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team with name {team.team_name} not updated")


# update manager_id in user table
def update_manager_id(user_id: int, manager_id: int | None = None):
    with Session(engine) as session:
        statement = select(User).where(
            User.id == user_id)
        results = session.exec(statement)
        user = results.first()
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User not found")
        user.manager_id = manager_id
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


#  remove team manager
def remove_team_manager(team: Team):
    with Session(engine) as session:
        try:
            team.manager_id = None
            session.add(team)
            session.commit()
            session.refresh(team)
            return team
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team with name {team.team_name} not updated")


# delete manager
def delete_manager(manager: Manager):
    update_manager_id(manager.user_id, None)
    with Session(engine) as session:
        try:
            session.delete(manager)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Manager with username {manager.username} not deleted")
        return {"status": "deleted"}


################################# Stadium Players Section #######################################################################################################
# get all stadium players
def all_stadiums_players():
    with Session(engine) as session:
        return session.exec(select(StadiumPlayerLink)).all()


# get all player stadiums
def get_player_stadiums(player: Player):
    with Session(engine) as session:
        statement = select(StadiumPlayerLink).where(
            StadiumPlayerLink.player_id == player.player_id)
        player_stadiums = session.exec(statement).all()
        if not player_stadiums:
            return None
        return player_stadiums


# get all stadium players
def get_stadium_players(stadium: Stadium):
    with Session(engine) as session:
        statement = select(StadiumPlayerLink).where(
            StadiumPlayerLink.stadium_id == stadium.stadium_id)
        stadium_players = session.exec(statement).all()
        if not stadium_players:
            return None
        return stadium_players


# get stadium player
def get_stadium_player(stadium_player: StadiumPlayerLink):
    with Session(engine) as session:
        statement = select(StadiumPlayerLink).where(
            StadiumPlayerLink.stadium_id == stadium_player.stadium_id).where(StadiumPlayerLink.player_id == stadium_player.player_id)
        stadium_player = session.exec(statement).first()
        if not stadium_player:
            return None
        return stadium_player


# add stadium player
def add_stadium_player(stadium_player: StadiumPlayerLink):
    with Session(engine) as session:
        try:
            db_stadium_player = StadiumPlayerLink.from_orm(
                StadiumPlayerLink(stadium_id=stadium_player.stadium_id, player_id=stadium_player.player_id))
            session.add(db_stadium_player)
            session.commit()
            session.refresh(db_stadium_player)
            return db_stadium_player
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Player with id {stadium_player.player_id} not added to stadium {stadium_player.stadium_id}")


# remove stadium player
def remove_stadium_player(stadium_player: StadiumPlayerLink):
    with Session(engine) as session:
        statement = select(StadiumPlayerLink).where(
            StadiumPlayerLink.stadium_id == stadium_player.stadium_id).where(StadiumPlayerLink.player_id == stadium_player.player_id)
        stadium_player = session.exec(statement).first()
        if not stadium_player:
            return None
        session.delete(stadium_player)
        session.commit()
        return stadium_player


# update stadium player
def update_stadium_player(stadium_player: StadiumPlayerLink):
    with Session(engine) as session:
        try:
            statement = select(StadiumPlayerLink).where(StadiumPlayerLink.stadium_id == stadium_player.stadium_id).where(
                StadiumPlayerLink.player_id == stadium_player.player_id)
            db_stadium_player = session.exec(statement).first()
            if not db_stadium_player:
                raise HTTPException(
                    status_code=404, detail=f"Player is not in stadium")
            stadium_player_dict = stadium_player.dict(exclude_unset=True)
            for key, value in stadium_player_dict.items():
                if value is not None:
                    setattr(db_stadium_player, key, value)
            session.add(db_stadium_player)
            session.commit()
            session.refresh(db_stadium_player)
            return db_stadium_player
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Stadium player not updated!")


################################## Match players section #############################################################################
# get all match players
def all_matches_players():
    with Session(engine) as session:
        return session.exec(select(MatchPlayerLink)).all()


# get all player matches
def get_player_matches(player: Player):
    with Session(engine) as session:
        statement = select(MatchPlayerLink).where(
            MatchPlayerLink.player_id == player.player_id)
        player_matches = session.exec(statement).all()
        if not player_matches:
            return None
        return player_matches


# get all match players
def get_match_players(match: Match):
    with Session(engine) as session:
        statement = select(MatchPlayerLink).where(
            MatchPlayerLink.match_id == match.match_id)
        match_players = session.exec(statement).all()
        if not match_players:
            return None
        return match_players


# get match player
def get_match_player(match_player: MatchPlayerLink):
    with Session(engine) as session:
        statement = select(MatchPlayerLink).where(
            MatchPlayerLink.match_id == match_player.match_id).where(MatchPlayerLink.player_id == match_player.player_id)
        match_player = session.exec(statement).first()
        if not match_player:
            return None
        return match_player


# add match player
def add_match_player(match_player: MatchPlayerLink):
    with Session(engine) as session:
        try:
            db_match_player = MatchPlayerLink.from_orm(
                MatchPlayerLink(match_id=match_player.match_id, player_id=match_player.player_id))
            session.add(db_match_player)
            session.commit()
            session.refresh(db_match_player)
            return db_match_player
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Player with id {match_player.player_id} not added to match {match_player.match_id}")


# remove match player
def remove_match_player(match_player: MatchPlayerLink):
    with Session(engine) as session:
        statement = select(MatchPlayerLink).where(
            MatchPlayerLink.match_id == match_player.match_id).where(MatchPlayerLink.player_id == match_player.player_id)
        match_player = session.exec(statement).first()
        if not match_player:
            return None
        session.delete(match_player)
        session.commit()
        return match_player


# update match player
def update_match_player(match_player: MatchPlayerLink):
    with Session(engine) as session:
        try:
            statement = select(MatchPlayerLink).where(MatchPlayerLink.match_id == match_player.match_id).where(
                MatchPlayerLink.player_id == match_player.player_id)
            db_match_player = session.exec(statement).first()
            if not db_match_player:
                raise HTTPException(
                    status_code=404, detail=f"Player is not in match")
            match_player_dict = match_player.dict(exclude_unset=True)
            for key, value in match_player_dict.items():
                if value is not None:
                    setattr(db_match_player, key, value)
            session.add(db_match_player)
            session.commit()
            session.refresh(db_match_player)
            return db_match_player
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match player not updated!")


# rate match player
def match_player_rating(match_player: MatchPlayerLink):
    with Session(engine) as session:
        statement = select(MatchPlayerLink).where(
            MatchPlayerLink.player_id == match_player.player_id)
        db_match_player = session.exec(statement).first()
        if not match_player:
            return None
        db_match_player.player_rating_count = db_match_player.player_rating_count + 1
        total_rating = db_match_player.player_rating * \
            db_match_player.player_rating_count
        total_rating += match_player.player_rating
        total_rating_average = total_rating / db_match_player.player_rating_count
        db_match_player.player_rating = round(total_rating_average, 2)
        session.add(db_match_player)
        session.commit()
        session.refresh(db_match_player)
        return db_match_player


# add a new match player goal scored
def add_match_player_goal(match_player: MatchPlayerLink):
    with Session(engine) as session:
        try:
            db_match_player = MatchPlayerLink.from_orm(
                MatchPlayerLink(match_id=match_player.match_id, player_id=match_player.player_id))
            db_match_player.player_goals = db_match_player.player_goals + 1
            session.add(db_match_player)
            session.commit()
            session.refresh(db_match_player)
            return db_match_player
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Player goal not added to match")


# add a new match player yellow card
def add_match_player_yellow_card(match_player: MatchPlayerLink):
    with Session(engine) as session:
        try:
            db_match_player = MatchPlayerLink.from_orm(
                MatchPlayerLink(match_id=match_player.match_id, player_id=match_player.player_id))
            db_match_player.player_yellow_cards = db_match_player.player_yellow_cards + 1
            session.add(db_match_player)
            session.commit()
            session.refresh(db_match_player)
            return db_match_player
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Player yellow card not added to match")


# add a new match player red card
def add_match_player_red_card(match_player: MatchPlayerLink):
    with Session(engine) as session:
        try:
            db_match_player = MatchPlayerLink.from_orm(
                MatchPlayerLink(match_id=match_player.match_id, player_id=match_player.player_id))
            db_match_player.player_red_cards = db_match_player.player_red_cards + 1
            session.add(db_match_player)
            session.commit()
            session.refresh(db_match_player)
            return db_match_player
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Player red card not added to match")


# add a new match player penalty
def add_match_player_penalty(match_player: MatchPlayerLink, penalty_scored: bool):
    with Session(engine) as session:
        try:
            db_match_player = MatchPlayerLink.from_orm(
                MatchPlayerLink(match_id=match_player.match_id, player_id=match_player.player_id))
            if penalty_scored:
                db_match_player.player_penalties_scored = db_match_player.player_penalties_scored + 1
            else:
                db_match_player.player_penalties_missed = db_match_player.player_penalties_missed + 1
            session.add(db_match_player)
            session.commit()
            session.refresh(db_match_player)
            return db_match_player
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Player penalty not added to match")


################################## Match Player Invitation Section ###############################################################################################
# get all match player invitations
def get_match_player_invitations():
    with Session(engine) as session:
        statement = select(PlayerMatchInvitation)
        match_player_invitations = session.exec(statement).all()
        if not match_player_invitations:
            return None
        return match_player_invitations


# get match player invitation
def get_match_player_invitation(player: Player, match: Match):
    with Session(engine) as session:
        statement = select(PlayerMatchInvitation).where(
            PlayerMatchInvitation.player_id == player.player_id and PlayerMatchInvitation.match_id == match.match_id)
        match_player_invitation = session.exec(statement).first()
        if not match_player_invitation:
            return None
        return match_player_invitation


# get all player matches invitations
def get_player_matches_invitations(player: Player):
    with Session(engine) as session:
        statement = select(PlayerMatchInvitation).where(
            PlayerMatchInvitation.player_id == player.player_id)
        match_player_invitations = session.exec(statement).all()
        if not match_player_invitations:
            return None
        return match_player_invitations


# get all match players invitations
def get_match_players_invitations(match: Match):
    with Session(engine) as session:
        statement = select(PlayerMatchInvitation).where(
            PlayerMatchInvitation.match_id == match.match_id)
        match_player_invitations = session.exec(statement).all()
        if not match_player_invitations:
            return None
        return match_player_invitations


# create a match player invitation
def add_match_player_invitation(match_player_invitation: PlayerMatchInvitation):
    with Session(engine) as session:
        try:
            new_match_player_invitation = PlayerMatchInvitation(
                **match_player_invitation.dict())
            session.add(new_match_player_invitation)
            session.commit()
            return new_match_player_invitation
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match player invitation with user ID {match_player_invitation.player_id} and match ID {match_player_invitation.match_id} not created")


# update a match player invitation
def update_match_player_invitation(match_player_invitation: PlayerMatchInvitation):
    with Session(engine) as session:
        try:
            statement = select(PlayerMatchInvitation).where(
                PlayerMatchInvitation.player_id == match_player_invitation.player_id).where(PlayerMatchInvitation.match_id == match_player_invitation.match_id)
            db_match_player_invitation = session.exec(statement).first()
            if not db_match_player_invitation:
                raise HTTPException(
                    status_code=404, detail=f"Match player invitation with user ID {match_player_invitation.player_id} and match ID {match_player_invitation.match_id} not found")
            match_player_invitation_dict = match_player_invitation.dict(
                exclude_unset=True)
            for key, value in match_player_invitation_dict.items():
                if value is not None:
                    setattr(db_match_player_invitation, key, value)
            session.add(db_match_player_invitation)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match player invitation with user ID {match_player_invitation.player_id} and match ID {match_player_invitation.match_id} not updated")


# remove a match player invitation
def remove_match_player_invitation(match_player_invitation: PlayerMatchInvitation):
    with Session(engine) as session:
        statement = select(PlayerMatchInvitation).where(
            PlayerMatchInvitation.player_id == match_player_invitation.player_id and PlayerMatchInvitation.match_id == match_player_invitation.match_id)
        match_player_invitation = session.exec(statement).first()
        if not match_player_invitation:
            return None
        session.delete(match_player_invitation)
        session.commit()
        return match_player_invitation


########################## Match Player Request Section #####################################################################################
# get all match player requests
def get_match_player_requests():
    with Session(engine) as session:
        statement = select(PlayerMatchRequest)
        match_player_requests = session.exec(statement).all()
        if not match_player_requests:
            return None
        return match_player_requests


# get match player request
def get_match_player_request(player: Player, match: Match):
    with Session(engine) as session:
        statement = select(PlayerMatchRequest).where(
            PlayerMatchRequest.player_id == player.player_id and PlayerMatchRequest.match_id == match.match_id)
        match_player_request = session.exec(statement).first()
        if not match_player_request:
            return None
        return match_player_request


# get all player matches requests
def get_player_matches_requests(player: Player):
    with Session(engine) as session:
        statement = select(PlayerMatchRequest).where(
            PlayerMatchRequest.player_id == player.player_id)
        match_player_requests = session.exec(statement).all()
        if not match_player_requests:
            return None
        return match_player_requests


# get all match players requests
def get_match_players_requests(match: Match):
    with Session(engine) as session:
        statement = select(PlayerMatchRequest).where(
            PlayerMatchRequest.match_id == match.match_id)
        match_player_requests = session.exec(statement).all()
        if not match_player_requests:
            return None
        return match_player_requests


# create a match player request
def add_match_player_request(match_player_request: PlayerMatchRequest):
    with Session(engine) as session:
        try:
            new_match_player_request = PlayerMatchRequest(
                **match_player_request.dict())
            session.add(new_match_player_request)
            session.commit()
            return new_match_player_request
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match player request with user ID {match_player_request.player_id} and match ID {match_player_request.match_id} not created")


# update a match player request
def update_match_player_request(match_player_request: PlayerMatchRequest):
    with Session(engine) as session:
        try:
            statement = select(PlayerMatchRequest).where(
                PlayerMatchRequest.player_id == match_player_request.player_id).where(PlayerMatchRequest.match_id == match_player_request.match_id)
            db_match_player_request = session.exec(statement).first()
            if not db_match_player_request:
                raise HTTPException(
                    status_code=404, detail=f"Match player request with user ID {match_player_request.player_id} and match ID {match_player_request.match_id} not found")
            match_player_request_dict = match_player_request.dict(
                exclude_unset=True)
            for key, value in match_player_request_dict.items():
                if value is not None:
                    setattr(db_match_player_request, key, value)
            session.add(db_match_player_request)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match player request with user ID {match_player_request.player_id} and match ID {match_player_request.match_id} not updated")


# remove a match player request
def remove_match_player_request(match_player_request: PlayerMatchRequest):
    with Session(engine) as session:
        statement = select(PlayerMatchRequest).where(
            PlayerMatchRequest.player_id == match_player_request.player_id and PlayerMatchRequest.match_id == match_player_request.match_id)
        match_player_request = session.exec(statement).first()
        if not match_player_request:
            return None
        session.delete(match_player_request)
        session.commit()
        return match_player_request


################################### Team Players Section ####################################################################################
# get all teams players
def all_teams_players():
    with Session(engine) as session:
        return session.exec(select(TeamPlayerLink)).all()


# get all player teams
def get_player_teams(player: Player):
    with Session(engine) as session:
        statement = select(TeamPlayerLink).where(
            TeamPlayerLink.player_id == player.player_id)
        player_teames = session.exec(statement).all()
        if not player_teames:
            return None
        return player_teames


# get all team players
def get_team_players(team: Team):
    with Session(engine) as session:
        statement = select(TeamPlayerLink).where(
            TeamPlayerLink.team_id == team.team_id)
        team_players = session.exec(statement).all()
        if not team_players:
            return None
        return team_players


# get team player
def get_team_player(team: Team, player: Player):
    with Session(engine) as session:
        statement = select(TeamPlayerLink).where(
            TeamPlayerLink.team_id == team.team_id).where(TeamPlayerLink.player_id == player.player_id)
        team_player = session.exec(statement).first()
        if not team_player:
            return None
        return team_player


# add team player
def add_team_player(team_player: TeamPlayerLink):
    with Session(engine) as session:
        try:
            db_team_player = TeamPlayerLink.from_orm(
                TeamPlayerLink(team_id=team_player.team_id, player_id=team_player.player_id))
            session.add(db_team_player)
            session.commit()
            session.refresh(db_team_player)
            return db_team_player
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Player with id {team_player.player_id} not added to team {team_player.team_id}")


# remove team player
def remove_team_player(team_player: TeamPlayerLink):
    with Session(engine) as session:
        statement = select(TeamPlayerLink).where(
            TeamPlayerLink.team_id == team_player.team_id).where(TeamPlayerLink.player_id == team_player.player_id)
        team_player = session.exec(statement).first()
        if not team_player:
            return None
        session.delete(team_player)
        session.commit()
        return team_player


# update team player
def update_team_player(team_player: TeamPlayerLink):
    with Session(engine) as session:
        try:
            statement = select(TeamPlayerLink).where(TeamPlayerLink.team_id == team_player.team_id).where(
                TeamPlayerLink.player_id == team_player.player_id)
            db_team_player = session.exec(statement).first()
            if not db_team_player:
                raise HTTPException(
                    status_code=404, detail=f"Player is not in team")
            team_player_dict = team_player.dict(exclude_unset=True)
            for key, value in team_player_dict.items():
                if value is not None:
                    setattr(db_team_player, key, value)
            session.add(db_team_player)
            session.commit()
            session.refresh(db_team_player)
            return db_team_player
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team player not updated!")


# get all team captains
def all_team_captains():
    with Session(engine) as session:
        return session.exec(select(TeamPlayerLink).where(
            TeamPlayerLink.is_captain == True)).all()


# get teams where player is captain
def player_captain_teams(player: Player):
    with Session(engine) as session:
        statement = select(TeamPlayerLink).where(
            TeamPlayerLink.is_captain == True).where(TeamPlayerLink.player_id == player.player_id)
        player_teams = session.exec(statement).all()
        if not player_teams:
            raise HTTPException(
                status_code=404, detail=f"Player with username {player.username} is not a captain of any team")
        return player_teams


# get team captain
def get_team_captain(team: Team):
    with Session(engine) as session:
        statement = select(TeamPlayerLink).where(
            TeamPlayerLink.player_id == team.captain_id)
        captain = session.exec(statement).first()
        if not captain:
            return None
        return captain


############################### Team Player Invitations Section ###############################################################################################
# get all players team invitations
def get_all_players_team_invitations():
    with Session(engine) as session:
        statement = select(PlayerTeamInvitation)
        team_player_invitations = session.exec(statement).all()
        if not team_player_invitations:
            return None
        return team_player_invitations


# get team player invitation
def get_team_player_invitation(player: Player, team: Team):
    with Session(engine) as session:
        statement = select(PlayerTeamInvitation).where(
            PlayerTeamInvitation.player_id == player.player_id and PlayerTeamInvitation.team_id == team.team_id)
        team_player_invitation = session.exec(statement).first()
        if not team_player_invitation:
            return None
        return team_player_invitation


# get player all teams invitations
def get_player_teams_invitations(player: Player):
    with Session(engine) as session:
        statement = select(PlayerTeamInvitation).where(
            PlayerTeamInvitation.player_id == player.player_id)
        team_player_invitations = session.exec(statement).all()
        if not team_player_invitations:
            return None
        return team_player_invitations


# get all team players invitations
def get_team_players_invitations(team: Team):
    with Session(engine) as session:
        statement = select(PlayerTeamInvitation).where(
            PlayerTeamInvitation.team_id == team.team_id)
        team_player_invitations = session.exec(statement).all()
        if not team_player_invitations:
            return None
        return team_player_invitations


# create a team player invitation
def add_team_player_invitation(team_player_invitation: PlayerTeamInvitation):
    with Session(engine) as session:
        try:
            new_team_player_invitation = PlayerTeamInvitation(
                **team_player_invitation.dict())
            session.add(new_team_player_invitation)
            session.commit()
            return new_team_player_invitation
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team player invitation with user ID {team_player_invitation.player_id} and team ID {team_player_invitation.team_id} not created")


# update a team player invitation
def update_team_player_invitation(team_player_invitation: PlayerTeamInvitation):
    with Session(engine) as session:
        try:
            statement = select(PlayerTeamInvitation).where(
                PlayerTeamInvitation.player_id == team_player_invitation.player_id).where(PlayerTeamInvitation.team_id == team_player_invitation.team_id)
            db_team_player_invitation = session.exec(statement).first()
            if not db_team_player_invitation:
                raise HTTPException(
                    status_code=404, detail=f"Team player invitation with user ID {team_player_invitation.player_id} and team ID {team_player_invitation.team_id} not found")
            team_player_invitation_dict = team_player_invitation.dict(
                exclude_unset=True)
            for key, value in team_player_invitation_dict.items():
                if value is not None:
                    setattr(db_team_player_invitation, key, value)
            session.add(db_team_player_invitation)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team player invitation with user ID {team_player_invitation.player_id} and team ID {team_player_invitation.team_id} not updated")


# remove a team player invitation
def remove_team_player_invitation(team_player_invitation: PlayerTeamInvitation):
    with Session(engine) as session:
        statement = select(PlayerTeamInvitation).where(
            PlayerTeamInvitation.player_id == team_player_invitation.player_id and PlayerTeamInvitation.team_id == team_player_invitation.team_id)
        team_player_invitation = session.exec(statement).first()
        if not team_player_invitation:
            return None
        session.delete(team_player_invitation)
        session.commit()
        return team_player_invitation


############################## Team Player Requests Section ##################################################################################################
# get all team players requests
def get_all_team_players_requests():
    with Session(engine) as session:
        statement = select(PlayerTeamRequest)
        team_player_requests = session.exec(statement).all()
        if not team_player_requests:
            return None
        return team_player_requests


# get team player request
def get_team_player_request(player: Player, team: Team):
    with Session(engine) as session:
        statement = select(PlayerTeamRequest).where(
            PlayerTeamRequest.player_id == player.player_id and PlayerTeamRequest.team_id == team.team_id)
        team_player_request = session.exec(statement).first()
        if not team_player_request:
            return None
        return team_player_request


# get all player teams requests
def get_player_teams_requests(player: Player):
    with Session(engine) as session:
        statement = select(PlayerTeamRequest).where(
            PlayerTeamRequest.player_id == player.player_id)
        team_player_requests = session.exec(statement).all()
        if not team_player_requests:
            return None
        return team_player_requests


# get all team players requests
def get_team_players_requests(team: Team):
    with Session(engine) as session:
        statement = select(PlayerTeamRequest).where(
            PlayerTeamRequest.team_id == team.team_id)
        team_player_requests = session.exec(statement).all()
        if not team_player_requests:
            return None
        return team_player_requests


# create a team player request
def add_team_player_request(team_player_request: PlayerTeamRequest):
    with Session(engine) as session:
        try:
            new_team_player_request = PlayerTeamRequest(
                **team_player_request.dict())
            session.add(new_team_player_request)
            session.commit()
            return new_team_player_request
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team player request with user ID {team_player_request.player_id} and team ID {team_player_request.team_id} not created")


# update a team player request
def update_team_player_request(team_player_request: PlayerTeamRequest):
    with Session(engine) as session:
        try:
            statement = select(PlayerTeamRequest).where(
                PlayerTeamRequest.player_id == team_player_request.player_id).where(PlayerTeamRequest.team_id == team_player_request.team_id)
            db_team_player_request = session.exec(statement).first()
            if not db_team_player_request:
                raise HTTPException(
                    status_code=404, detail=f"Team player request with user ID {team_player_request.player_id} and team ID {team_player_request.team_id} not found")
            team_player_request_dict = team_player_request.dict(
                exclude_unset=True)
            for key, value in team_player_request_dict.items():
                if value is not None:
                    setattr(db_team_player_request, key, value)
            session.add(db_team_player_request)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team player request with user ID {team_player_request.player_id} and team ID {team_player_request.team_id} not updated")


# remove a team player request
def remove_team_player_request(team_player_request: PlayerTeamRequest):
    with Session(engine) as session:
        statement = select(PlayerTeamRequest).where(
            PlayerTeamRequest.player_id == team_player_request.player_id and PlayerTeamRequest.team_id == team_player_request.team_id)
        team_player_request = session.exec(statement).first()
        if not team_player_request:
            return None
        session.delete(team_player_request)
        session.commit()
        return team_player_request


############################## Coach Player Requests Section ##################################################################################################
# get all coach player requests
def get_coach_player_requests():
    with Session(engine) as session:
        statement = select(PlayerCoachRequest)
        coach_player_requests = session.exec(statement).all()
        if not coach_player_requests:
            return None
        return coach_player_requests


# get coach player request
def get_coach_player_request(player: Player, coach: Coach):
    with Session(engine) as session:
        statement = select(PlayerCoachRequest).where(
            PlayerCoachRequest.player_id == player.player_id and PlayerCoachRequest.coach_id == coach.coach_id)
        coach_player_request = session.exec(statement).first()
        if not coach_player_request:
            return None
        return coach_player_request


# get all player coachs requests
def get_player_coachs_requests(player: Player):
    with Session(engine) as session:
        statement = select(PlayerCoachRequest).where(
            PlayerCoachRequest.player_id == player.player_id)
        coach_player_requests = session.exec(statement).all()
        if not coach_player_requests:
            return None
        return coach_player_requests


# get all coach players requests
def get_coach_players_requests(coach: Coach):
    with Session(engine) as session:
        statement = select(PlayerCoachRequest).where(
            PlayerCoachRequest.coach_id == coach.coach_id)
        coach_player_requests = session.exec(statement).all()
        if not coach_player_requests:
            return None
        return coach_player_requests


# create a coach player request
def add_coach_player_request(coach_player_request: PlayerCoachRequest):
    with Session(engine) as session:
        try:
            new_coach_player_request = PlayerCoachRequest(
                **coach_player_request.dict())
            session.add(new_coach_player_request)
            session.commit()
            return new_coach_player_request
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Coach player request with user ID {coach_player_request.player_id} and coach ID {coach_player_request.coach_id} not created")


# update a coach player request
def update_coach_player_request(coach_player_request: PlayerCoachRequest):
    with Session(engine) as session:
        try:
            statement = select(PlayerCoachRequest).where(
                PlayerCoachRequest.player_id == coach_player_request.player_id).where(PlayerCoachRequest.coach_id == coach_player_request.coach_id)
            db_coach_player_request = session.exec(statement).first()
            if not db_coach_player_request:
                raise HTTPException(
                    status_code=404, detail=f"Coach player request with user ID {coach_player_request.player_id} and coach ID {coach_player_request.coach_id} not found")
            coach_player_request_dict = coach_player_request.dict(
                exclude_unset=True)
            for key, value in coach_player_request_dict.items():
                if value is not None:
                    setattr(db_coach_player_request, key, value)
            session.add(db_coach_player_request)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Coach player request with user ID {coach_player_request.player_id} and coach ID {coach_player_request.coach_id} not updated")


# remove a coach player request
def remove_coach_player_request(coach_player_request: PlayerCoachRequest):
    with Session(engine) as session:
        statement = select(PlayerCoachRequest).where(
            PlayerCoachRequest.player_id == coach_player_request.player_id and PlayerCoachRequest.coach_id == coach_player_request.coach_id)
        coach_player_request = session.exec(statement).first()
        if not coach_player_request:
            return None
        session.delete(coach_player_request)
        session.commit()
        return coach_player_request


################################### Players Availabilities Section ##################################################################################
# get all players availabilities
def all_players_availabilities():
    with Session(engine) as session:
        return session.exec(select(PlayerAvailability)).all()


# check if player is available at a specific time
def check_player_availability(player: Player, available_from: datetime, available_to: datetime):
    with Session(engine) as session:
        statement = select(PlayerAvailability).where(PlayerAvailability.player_id == player.player_id,
                                                     PlayerAvailability.available_from <= available_from, PlayerAvailability.available_to >= available_to)
        availability = session.exec(statement).first()
        if not availability:
            return False
        return True


# set player availability
def add_player_availability(player: Player, available_from: datetime, available_to: datetime):
    with Session(engine) as session:
        try:
            availability = PlayerAvailability(
                player_id=player.player_id, available_from=available_from, available_to=available_to)
            session.add(availability)
            session.commit()
            return availability
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Player availability with user ID {player.player_id} not created")


# get players by availability date and time range
def get_players_by_availability(available_from: datetime, available_to: datetime):
    with Session(engine) as session:
        statement = select(PlayerAvailability).where(
            PlayerAvailability.available_from <= available_from,
            PlayerAvailability.available_to >= available_to
        )
        players = session.exec(statement).all()
        if not players:
            return None
        return players


# get player availabilities
def get_player_availabilities(player: Player):
    with Session(engine) as session:
        statement = select(PlayerAvailability).where(
            PlayerAvailability.player_id == player.player_id)
        availabilities = session.exec(statement).all()
        if not availabilities:
            return None
        return availabilities


# get player availability
def get_player_availability(player: Player, available_from: datetime):
    with Session(engine) as session:
        statement = select(PlayerAvailability).where(
            PlayerAvailability.player_id == player.player_id, PlayerAvailability.available_from == available_from)
        availability = session.exec(statement).first()
        if not availability:
            return None
        return availability


# update player availability
def update_player_availability(availability: PlayerAvailability):
    with Session(engine) as session:
        try:
            availability_db = get_player_availability(
                availability.player_id, availability.available_from)
            if not availability_db:
                raise HTTPException(
                    status_code=404, detail=f"Player availability with user ID {availability.player_id} and available from {availability.available_from} not found")
            availability_dict = availability.dict(exclude_unset=True)
            for key, value in availability_dict.items():
                if value is not None:
                    setattr(availability_db, key, value)
            session.add(availability_db)
            session.commit()
            session.refresh(availability_db)
            return availability_db
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Player availability with user ID {availability.player_id} and available from {availability.available_from} already exists")
        except Exception as e:
            session.rollback()
            raise e


# delete player availability
def delete_player_availability(availability: PlayerAvailability):
    with Session(engine) as session:
        try:
            session.delete(availability)
            session.commit()
            return {"status": "deleted"}
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Player availability with user ID {availability.player_id} and available from {availability.available_from} not deleted")


# delete all player availabilities
def delete_all_player_availabilities(player: Player):
    with Session(engine) as session:
        try:
            availabilities = session.exec(select(PlayerAvailability).where(
                PlayerAvailability.player_id == player.player_id)).all()
            if not availabilities:
                raise HTTPException(
                    status_code=404, detail=f"Player availabilities not found")
            session.delete(availabilities)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=str(e))


################################### Players section ##################################################################################
# get all players
def all_players():
    with Session(engine) as session:
        return session.exec(select(Player)).all()


# create player
def create_player(new_player: Player):
    with Session(engine) as session:
        try:
            db_player = Player.from_orm(new_player)
            session.add(db_player)
            session.commit()
            session.refresh(db_player)
            update_player_id(new_player.user_id, db_player.player_id)
            return db_player
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(e))


# get player
def get_player(username: str):
    with Session(engine) as session:
        statement = select(Player).where(Player.username == username)
        player = session.exec(statement).first()
        if not player:
            return None
        return player


# get player join_team preference
def player_join_team(player: Player):
    with Session(engine) as session:
        statement = select(Player).where(Player.player_id == player.player_id)
        db_player = session.exec(statement).first()
        if not db_player:
            raise HTTPException(
                status_code=404, detail=f"Player with user ID {player.player_id} not found")
        return db_player.join_team


# get player join_match preference
def player_join_match(player: Player):
    with Session(engine) as session:
        statement = select(Player).where(Player.player_id == player.player_id)
        db_player = session.exec(statement).first()
        if not db_player:
            raise HTTPException(
                status_code=404, detail=f"Player with user ID {player.player_id} not found")
        return db_player.join_match


# get player rating
def get_player_rating(player: Player):
    with Session(engine) as session:
        statement = select(Player).where(Player.player_id == player.player_id)
        db_player = session.exec(statement).first()
        if not db_player:
            return None
        return {"rating count": db_player.total_rating_count, "rating": db_player.total_rating}


# get players by join_team preference
def get_players_by_join_team(join_team: bool):
    with Session(engine) as session:
        statement = select(Player).where(Player.join_team == join_team)
        players = session.exec(statement).all()
        if not players:
            return None
        return players


# get players by join_match preference
def get_players_by_join_match(join_match: bool):
    with Session(engine) as session:
        statement = select(Player).where(Player.join_match == join_match)
        players = session.exec(statement).all()
        if not players:
            return None
        return players


# get players by rating
def get_players_by_rating(rating: int):
    with Session(engine) as session:
        statement = select(Player).where(Player.total_rating >= rating)
        players = session.exec(statement).all()
        if not players:
            raise HTTPException(
                status_code=404, detail=f"No players found with rating {rating}")
        return players


# get players by favorite position
def get_players_by_favorite_position(favorite_position: str):
    with Session(engine) as session:
        statement = select(Player).where(
            Player.favorite_position == favorite_position)
        players = session.exec(statement).all()
        if not players:
            raise HTTPException(
                status_code=404, detail=f"No players found with favorite position {favorite_position}")
        return players


# get players in a radius
def get_players_in_radius(longitude: float, latitude: float, radius: float):
    search_area = get_search_area(
        latitude=latitude, longitude=longitude, radius=radius)
    with Session(engine) as session:
        # Query players within the specified radius
        players = session.exec(select(Player).where(
            Player.player_longitude >= search_area['min_longitude'],
            Player.player_longitude <= search_area['max_longitude'],
            Player.player_latitude >= search_area['min_latitude'],
            Player.player_latitude <= search_area['max_latitude']
        )).all()

        if not players:
            raise HTTPException(
                status_code=404, detail=f"No players found within {radius} km radius")
        return players


# get players by rating and location radius
def get_players_by_rating_radius(rating: int, longitude: float, latitude: float, radius: float):
    with Session(engine) as session:
        # get players within the specified radius
        players = get_players_in_radius(longitude, latitude, radius)
        if not players:
            raise HTTPException(
                status_code=404, detail=f"No players found within {radius} km radius")
        # filter players by rating
        found_players = list(
            filter(lambda found_player: found_player.total_rating >= rating, players))
        if not found_players:
            raise HTTPException(
                status_code=404, detail=f"No players found with at least a rating of {rating} and within {radius} km radius")
        return found_players


# get players by favorite position and location radius
def get_players_by_position_in_radius(longitude: float, latitude: float, favorite_position: str, radius: float):
    with Session(engine) as session:
        # get players within the specified radius
        players = get_players_in_radius(longitude, latitude, radius)
        if not players:
            raise HTTPException(
                status_code=404, detail=f"No players found within {radius} km radius")
        # filter players by favorite position
        found_players = list(
            filter(lambda found_player: found_player.favorite_position == favorite_position, players))
        if not found_players:
            raise HTTPException(
                status_code=404, detail=f"No players found with favorite position {favorite_position} and within {radius} km radius")
        return found_players


# update player
def update_player(player: PlayerUpdate):
    with Session(engine) as session:
        try:
            player_db = get_player(player.username)
            if not player_db:
                raise HTTPException(
                    status_code=404, detail=f"Player with username {player.username} not found")
            player_dict = player.dict(exclude_unset=True)
            for key, value in player_dict.items():
                if value is not None:
                    setattr(player_db, key, value)
            session.add(player_db)
            session.commit()
            session.refresh(player_db)
            return player_db
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Player with username {player.username} did not update!")


# update player_id in user table
def update_player_id(user_id: int, player_id: int | None = None):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User not found")
        user.player_id = player_id
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


# update player rating
def update_player_rating(player: Player):
    with Session(engine) as session:
        statement = select(MatchPlayerLink).where(
            MatchPlayerLink.player_id == player.player_id)
        player_matches = session.exec(statement).all()
        if not player_matches:
            return None
        for player_match in player_matches:
            total_rating_count = player.total_rating_count + 1
            total_rating = player.total_rating * player.total_rating_count
            total_rating += player_match.player_rating
            total_rating_average = total_rating / total_rating_count
            total_rating_average = round(total_rating_average, 2)

            matches_count = player.total_matches_played + 1
            total_matches = matches_count + total_matches
            goals_count = player.total_goals + player_match.player_goals
            total_goals = goals_count + total_goals
            assissts_count = player.total_assists + player_match.player_assists
            total_assists = assissts_count + total_assists
            yellow_cards_count = player.total_yellow_cards + player_match.player_yellow_cards
            total_yellow_cards = yellow_cards_count + total_yellow_cards
            red_cards_count = player.total_red_cards + player_match.player_red_cards
            total_red_cards = red_cards_count + total_red_cards
            penalties_scored_count = player.total_penalties_scored + \
                player_match.player_penalties_scored
            penalties_scored_total = penalties_scored_count + penalties_scored_total
            penalties_missed_count = player.total_penalties_missed + \
                player_match.player_penalties_missed
            penalties_missed_total = penalties_missed_count + penalties_missed_total

            player.total_rating_count = total_rating_count
            player.total_rating = total_rating_average
            player.total_matches_played = total_matches
            player.total_goals = total_goals
            player.total_assists = total_assists
            player.total_yellow_cards = total_yellow_cards
            player.total_red_cards = total_red_cards
            player.total_penalties_scored = penalties_scored_total
            player.total_penalties_missed = penalties_missed_total

            session.add(player)
            session.commit()
            session.refresh(player)
            return player


# delete player
def delete_player(player: Player):
    with Session(engine) as session:
        try:
            session.delete(player)
            session.commit()
            return {"status": "deleted"}
        except:
            session.rollback()
        raise HTTPException(
            status_code=404, detail=f"{player.username} not deleted!")


####################################### Stadium Teams Section ##############################################################################
# get all team stadiums
def get_team_stadiums(team: Team):
    with Session(engine) as session:
        statement = select(StadiumTeamLink).where(
            StadiumTeamLink.team_id == team.team_id)
        team_stadiums = session.exec(statement).all()
        if not team_stadiums:
            return None
        return team_stadiums


# get all stadium teams
def get_stadium_teams(stadium: Stadium):
    with Session(engine) as session:
        statement = select(StadiumTeamLink).where(
            StadiumTeamLink.stadium_id == stadium.stadium_id)
        stadium_teams = session.exec(statement).all()
        if not stadium_teams:
            return None
        return stadium_teams


# get stadium team
def get_stadium_team(stadium_id: int, team_id: int):
    with Session(engine) as session:
        stadium_team = session.exec(select(StadiumTeamLink).where(
            StadiumTeamLink.stadium_id == stadium_id).where(StadiumTeamLink.team_id == team_id)).first()
        if not stadium_team:
            return None
        return stadium_team


# add stadium team
def add_stadium_team(stadium_id: int, team_id: int):
    with Session(engine) as session:
        try:
            stadium_team = StadiumTeamLink.from_orm(
                StadiumTeamLink(stadium_id=stadium_id, team_id=team_id))
            session.add(stadium_team)
            session.commit()
            session.refresh(stadium_team)
            return stadium_team
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=str(e))


# remove stadium team
def remove_stadium_team(stadium_team: StadiumTeamLink):
    with Session(engine) as session:
        try:
            session.delete(stadium_team)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=str(e))


# update stadium team
def update_stadium_team(stadium_team: StadiumTeamLink):
    with Session(engine) as session:
        try:
            stadium_team_dict = stadium_team.dict(exclude_unset=True)
            for key, value in stadium_team_dict.items():
                if value is not None:
                    setattr(stadium_team, key, value)
            session.add(stadium_team)
            session.commit()
            session.refresh(stadium_team)
            return stadium_team
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=str(e))


# assign home stadium
def assign_home_stadium(team: Team, stadium: Stadium):
    with Session(engine) as session:
        try:
            team.home_stadium_id = stadium.stadium_id
            session.add(team)
            session.commit()
            session.refresh(team)
            return team
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=str(e))


# remove home stadium
def remove_home_stadium(team: Team):
    with Session(engine) as session:
        try:
            team.home_stadium_id = None
            session.add(team)
            session.commit()
            session.refresh(team)
            return team
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=str(e))


# update home_team
def update_home_team(stadium_team: StadiumTeamLink, home_team: bool):
    with Session(engine) as session:
        try:
            stadium_team.home_team = home_team
            session.add(stadium_team)
            session.commit()
            session.refresh(stadium_team)
            return stadium_team
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=str(e))


##################################### Team Matches Section ##################################################################################################################
# get all matches teams
def all_matches_teams():
    with Session(engine) as session:
        return session.exec(select(MatchTeamLink)).all()


# get all team matches
def get_team_matches(team: Team):
    with Session(engine) as session:
        statement = select(MatchTeamLink).where(
            MatchTeamLink.team_id == team.team_id)
        team_matches = session.exec(statement).all()
        if not team_matches:
            return None
        return team_matches


# get match teams
def get_match_teams(match: Match):
    with Session(engine) as session:
        statement = select(Match).where(
            Match.match_id == match.match_id)
        match = session.exec(statement).all()
        if not match:
            return None
        return {"home_team": match.home_team_name, "away_team": match.away_team_name}


# get match home team
def get_match_team(match: Match, team: Team):
    with Session(engine) as session:
        statement = select(MatchTeamLink).where(
            MatchTeamLink.match_id == match.match_id).where(MatchTeamLink.team_id == team.team_id)
        match_team = session.exec(statement).first()
        if not match_team:
            return None
        return match_team


# remove match team
def remove_match_team(match_team: MatchTeamLink):
    with Session(engine) as session:
        statement = select(MatchTeamLink).where(
            MatchTeamLink.match_id == match_team.match_id).where(MatchTeamLink.team_id == match_team.team_id)
        match_team = session.exec(statement).first()
        if not match_team:
            return None
        session.delete(match_team)
        session.commit()
        return match_team

# rate match team


def match_team_rating(match_team: MatchTeamLink):
    with Session(engine) as session:
        statement = select(MatchTeamLink).where(
            MatchTeamLink.team_id == match_team.team_id)
        db_match_team = session.exec(statement).first()
        if not match_team:
            return None
        db_match_team.team_rating_count = db_match_team.team_rating_count + 1
        total_rating = db_match_team.team_rating * db_match_team.team_rating_count
        total_rating += match_team.team_rating
        total_rating_average = total_rating / db_match_team.team_rating_count
        db_match_team.team_rating = round(total_rating_average, 2)
        session.add(db_match_team)
        session.commit()
        session.refresh(db_match_team)
        return db_match_team


# add a new match team
def add_match_team(match: Match, team: Team, is_home_team: bool):
    with Session(engine) as session:
        try:
            db_match_team = MatchTeamLink.from_orm(
                MatchTeamLink(match_id=match.match_id, team_id=team.team_id, manager_id=team.manager_id, is_home_team=is_home_team))
            session.add(db_match_team)
            session.commit()
            session.refresh(db_match_team)
            return db_match_team
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail="Team not added")


# add a new match team goal scored
def add_match_team_goal(match: Match, scoring_team_id: int):
    with Session(engine) as session:
        try:
            db_match_team = MatchTeamLink.from_orm(
                MatchTeamLink(match_id=match.match_id, team_id=scoring_team_id))
            db_match_team.team_goals_scored = db_match_team.team_goals_scored + 1
            session.add(db_match_team)
            session.commit()
            session.refresh(db_match_team)
            return db_match_team
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail="Team goal not added")


# add a new match team goal conceded
def add_match_team_goal_conceded(match: Match, conceded_team_id: int):
    with Session(engine) as session:
        try:
            db_match_team = MatchTeamLink.from_orm(
                MatchTeamLink(match_id=match.match_id, team_id=conceded_team_id))
            db_match_team.team_goals_conceded = db_match_team.team_goals_conceded + 1
            session.add(db_match_team)
            session.commit()
            session.refresh(db_match_team)
            return db_match_team
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail="Team goal not added")


# add a new match team yellow card
def add_match_team_yellow_card(match_team: MatchTeamLink):
    with Session(engine) as session:
        try:
            db_match_team = MatchTeamLink.from_orm(
                MatchTeamLink(match_id=match_team.match_id, team_id=match_team.team_id))
            db_match_team.team_yellow_cards = db_match_team.team_yellow_cards + 1
            session.add(db_match_team)
            session.commit()
            session.refresh(db_match_team)
            return db_match_team
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Team yellow card not added to match")


# add a new match team red card
def add_match_team_red_card(match_team: MatchTeamLink):
    with Session(engine) as session:
        try:
            db_match_team = MatchTeamLink.from_orm(
                MatchTeamLink(match_id=match_team.match_id, team_id=match_team.team_id))
            db_match_team.team_red_cards = db_match_team.team_red_cards + 1
            session.add(db_match_team)
            session.commit()
            session.refresh(db_match_team)
            return db_match_team
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Team red card not added to match")


# add a new match team penalty scored
def add_match_team_penalty_scored(match: Match, scoring_team_id: int):
    with Session(engine) as session:
        try:
            db_match_team = MatchTeamLink.from_orm(
                MatchTeamLink(match_id=match.match_id, team_id=scoring_team_id))
            db_match_team.team_penalties_scored = db_match_team.team_penalties_scored + 1
            db_match_team.team_goals_scored = db_match_team.team_goals_scored + 1
            session.add(db_match_team)
            session.commit()
            session.refresh(db_match_team)
            return db_match_team
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail="Team goal not added")


# add a new match team penalty missed
def add_match_team_penalty_missed(match: Match, scoring_team_id: int):
    with Session(engine) as session:
        try:
            db_match_team = MatchTeamLink.from_orm(
                MatchTeamLink(match_id=match.match_id, team_id=scoring_team_id))
            db_match_team.team_penalties_missed = db_match_team.team_penalties_missed + 1
            session.add(db_match_team)
            session.commit()
            session.refresh(db_match_team)
            return db_match_team
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail="Team goal not added")


############################## Match Team Invitation Section ################################################################################
# get all team match invitations
def get_team_matches_invitations(team: Team, match: Match):
    with Session(engine) as session:
        statement = select(TeamMatchInvitation).where(
            TeamMatchInvitation.team_id == team.team_id)
        team_match_invitations = session.exec(statement).all()
        if not team_match_invitations:
            return None
        return team_match_invitations


# get team match invitation
def get_team_match_invitation(team: Team, match: Match):
    with Session(engine) as session:
        statement = select(TeamMatchInvitation).where(
            TeamMatchInvitation.team_id == team.team_id and TeamMatchInvitation.match_id == match.match_id)
        team_match_invitation = session.exec(statement).first()
        if not team_match_invitation:
            return None
        return team_match_invitation


# get all team matches invitations
def get_team_matches_invitations(team_name: str):
    with Session(engine) as session:
        statement = select(TeamMatchInvitation).where(
            TeamMatchInvitation.team_name == team_name)
        team_matches_invitations = session.exec(statement).all()
        if not team_matches_invitations:
            return None
        return team_matches_invitations


# create team match invitation
def add_team_match_invitation(team_match_invitation: TeamMatchInvitation):
    with Session(engine) as session:
        try:
            new_team_match_invitation = TeamMatchInvitation(
                **team_match_invitation.dict())
            session.add(new_team_match_invitation)
            session.commit()
            return new_team_match_invitation
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team match invitation with team name {team_match_invitation.team_name} and match ID {team_match_invitation.match_id} not created")


# remove team match invitation
def remove_team_match_invitation(team_match_invitation: TeamMatchInvitation):
    with Session(engine) as session:
        try:
            session.delete(team_match_invitation)
            session.commit()
            return team_match_invitation
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team match invitation with team name {team_match_invitation.team_name} and match ID {team_match_invitation.match_id} not deleted")

######################################## Match Team Request Section ###########################################################################################################
# get all match team requests


def get_match_team_requests():
    with Session(engine) as session:
        statement = select(TeamMatchRequest)
        match_team_requests = session.exec(statement).all()
        if not match_team_requests:
            return None
        return match_team_requests


# get match team request
def get_match_team_request(team: Team, match: Match):
    with Session(engine) as session:
        statement = select(TeamMatchRequest).where(
            TeamMatchRequest.team_id == team.team_id and TeamMatchRequest.match_id == match.match_id)
        match_team_request = session.exec(statement).first()
        if not match_team_request:
            return None
        return match_team_request


# get all team matches requests
def get_team_matches_requests(team: Team):
    with Session(engine) as session:
        statement = select(TeamMatchRequest).where(
            TeamMatchRequest.team_id == team.team_id)
        match_team_requests = session.exec(statement).all()
        if not match_team_requests:
            return None
        return match_team_requests


# get all match teams requests
def get_match_teams_requests(match: Match):
    with Session(engine) as session:
        statement = select(TeamMatchRequest).where(
            TeamMatchRequest.match_id == match.match_id)
        match_team_requests = session.exec(statement).all()
        if not match_team_requests:
            return None
        return match_team_requests


# create a match team request
def add_match_team_request(match_team_request: TeamMatchRequest):
    with Session(engine) as session:
        try:
            new_match_team_request = TeamMatchRequest(
                **match_team_request.dict())
            session.add(new_match_team_request)
            session.commit()
            return new_match_team_request
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match team request with user ID {match_team_request.team_id} and match ID {match_team_request.match_id} not created")


# update a match team request
def update_match_team_request(match_team_request: TeamMatchRequest):
    with Session(engine) as session:
        try:
            statement = select(TeamMatchRequest).where(
                TeamMatchRequest.team_id == match_team_request.team_id).where(TeamMatchRequest.match_id == match_team_request.match_id)
            db_match_team_request = session.exec(statement).first()
            if not db_match_team_request:
                raise HTTPException(
                    status_code=404, detail=f"Match team request with user ID {match_team_request.team_id} and match ID {match_team_request.match_id} not found")
            match_team_request_dict = match_team_request.dict(
                exclude_unset=True)
            for key, value in match_team_request_dict.items():
                if value is not None:
                    setattr(db_match_team_request, key, value)
            session.add(db_match_team_request)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match team request with user ID {match_team_request.team_id} and match ID {match_team_request.match_id} not updated")


# remove a match team request
def remove_match_team_request(match_team_request: TeamMatchRequest):
    with Session(engine) as session:
        statement = select(TeamMatchRequest).where(
            TeamMatchRequest.team_id == match_team_request.team_id and TeamMatchRequest.match_id == match_team_request.match_id)
        match_team_request = session.exec(statement).first()
        if not match_team_request:
            return None
        session.delete(match_team_request)
        session.commit()
        return match_team_request


############################## Team Coach Requests Section ##################################################################################################
# get all teams coaches requests
def get_all_teams_coaches_requests():
    with Session(engine) as session:
        statement = select(TeamCoachRequest)
        team_coach_requests = session.exec(statement).all()
        if not team_coach_requests:
            return None
        return team_coach_requests


# get team coach request
def get_team_coach_request(coach: Coach, team: Team):
    with Session(engine) as session:
        statement = select(TeamCoachRequest).where(
            TeamCoachRequest.coach_id == coach.coach_id and TeamCoachRequest.team_id == team.team_id)
        team_coach_request = session.exec(statement).first()
        if not team_coach_request:
            return None
        return team_coach_request


# get all coach teams requests
def get_coach_teams_requests(coach: Coach):
    with Session(engine) as session:
        statement = select(TeamCoachRequest).where(
            TeamCoachRequest.coach_id == coach.coach_id)
        team_coach_requests = session.exec(statement).all()
        if not team_coach_requests:
            return None
        return team_coach_requests


# get all team coaches requests
def get_team_coaches_requests(team: Team):
    with Session(engine) as session:
        statement = select(TeamCoachRequest).where(
            TeamCoachRequest.team_id == team.team_id)
        team_coach_requests = session.exec(statement).all()
        if not team_coach_requests:
            return None
        return team_coach_requests


# create a team coach request
def add_team_coach_request(team_coach_request: TeamCoachRequest):
    with Session(engine) as session:
        try:
            new_team_coach_request = TeamCoachRequest(
                **team_coach_request.dict())
            session.add(new_team_coach_request)
            session.commit()
            return new_team_coach_request
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team coach request with user ID {team_coach_request.coach_id} and team ID {team_coach_request.team_id} not created")


# update a team coach request
def update_team_coach_request(team_coach_request: TeamCoachRequest):
    with Session(engine) as session:
        try:
            statement = select(TeamCoachRequest).where(
                TeamCoachRequest.coach_id == team_coach_request.coach_id).where(TeamCoachRequest.team_id == team_coach_request.team_id)
            db_team_coach_request = session.exec(statement).first()
            if not db_team_coach_request:
                raise HTTPException(
                    status_code=404, detail=f"Team coach request with user ID {team_coach_request.coach_id} and team ID {team_coach_request.team_id} not found")
            team_coach_request_dict = team_coach_request.dict(
                exclude_unset=True)
            for key, value in team_coach_request_dict.items():
                if value is not None:
                    setattr(db_team_coach_request, key, value)
            session.add(db_team_coach_request)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team coach request with user ID {team_coach_request.coach_id} and team ID {team_coach_request.team_id} not updated")


# remove a team coach request
def remove_team_coach_request(team_coach_request: TeamCoachRequest):
    with Session(engine) as session:
        statement = select(TeamCoachRequest).where(
            TeamCoachRequest.coach_id == team_coach_request.coach_id and TeamCoachRequest.team_id == team_coach_request.team_id)
        team_coach_request = session.exec(statement).first()
        if not team_coach_request:
            return None
        session.delete(team_coach_request)
        session.commit()
        return team_coach_request


################################### Teams Availabilities Section ##################################################################################
# get all teams availabilities
def all_teams_availabilities():
    with Session(engine) as session:
        return session.exec(select(TeamAvailability)).all()


# check if team is available at a specific time
def check_team_availability(team: Team, available_from: datetime, available_to: datetime):
    with Session(engine) as session:
        statement = select(TeamAvailability).where(TeamAvailability.team_id == team.team_id,
                                                   TeamAvailability.available_from <= available_from, TeamAvailability.available_to >= available_to)
        availability = session.exec(statement).first()
        if not availability:
            return False
        return True


# set team availability
def add_team_availability(team_availability: TeamAvailability):
    with Session(engine) as session:
        try:
            session.add(team_availability)
            session.commit()
            return team_availability
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team availability for team {team_availability.team_id} not created")


# Calculate Team Availability based on team players availability on a specific date and update the team availability accordingly
def add_match_date_availability(team: Team, match_date: datetime):
    with Session(engine) as session:
        # Get all players of the team
        statement = select(TeamPlayerLink).where(
            TeamPlayerLink.team_id == team.team_id)
        team_players = session.exec(statement).all()
        if not team_players:
            return None

        # Get the availability of each player and their time ranges on the specified match_date
        availability_count_per_time = {}
        for team_player in team_players:
            player = team_player
            # To avoid lazy loading for availability, expunge the team_player
            session.expunge(team_player)

            # Use selectinload to fetch the player's availability directly in the same query to avoid N+1 query issue.
            statement = select(PlayerAvailability).options(selectinload(Player.availabilities)).where(
                PlayerAvailability.player_id == player.player_id
            )
            availabilities = session.exec(statement).all()

            for availability in availabilities:
                if availability.available_from.date() <= match_date.date() <= availability.available_to.date():
                    # Calculate the number of available players for each minute within the player's availability time range on match_date
                    current_time = max(availability.available_from, datetime.combine(
                        match_date, datetime.min.time()))
                    end_time = min(availability.available_to, datetime.combine(
                        match_date, datetime.max.time()))
                    while current_time <= end_time:
                        if current_time not in availability_count_per_time:
                            availability_count_per_time[current_time] = 0
                        availability_count_per_time[current_time] += 1
                        current_time += timedelta(minutes=1)

        # Find the match time with the maximum number of available players on the specified date
        max_available_time = max(
            availability_count_per_time, key=availability_count_per_time.get)
        max_available_players_count = availability_count_per_time[max_available_time]
        if max_available_players_count == 0:
            return None
        # update team availability based on the calculated availability
        team_availability = TeamAvailability(
            team_id=team.team_id, available_from=max_available_time, available_to=max_available_time + timedelta(minutes=60), available_players_count=max_available_players_count)
        return add_team_availability(team_availability)


# get teams by availability date and time range
def get_teams_by_availability(available_from: datetime, available_to: datetime):
    with Session(engine) as session:
        statement = select(TeamAvailability).where(
            TeamAvailability.available_from <= available_from,
            TeamAvailability.available_to >= available_to
        )
        teams = session.exec(statement).all()
        if not teams:
            return None
        return teams


# get team availabilities
def get_team_availabilities(team: Team):
    with Session(engine) as session:
        statement = select(TeamAvailability).where(
            TeamAvailability.team_id == team.team_id)
        availabilities = session.exec(statement).all()
        if not availabilities:
            return None
        return availabilities


# get team availability
def get_team_availability(team: Team, available_from: datetime):
    with Session(engine) as session:
        statement = select(TeamAvailability).where(
            TeamAvailability.team_id == team.team_id, TeamAvailability.available_from == available_from)
        availability = session.exec(statement).first()
        if not availability:
            return None
        return availability


# update team availability
def update_team_availability(availability: TeamAvailability):
    with Session(engine) as session:
        try:
            availability_db = get_team_availability(
                availability.team_id, availability.available_from)
            if not availability_db:
                raise HTTPException(
                    status_code=404, detail=f"Team availability with team ID {availability.team_id} and available from {availability.available_from} not found")
            availability_dict = availability.dict(exclude_unset=True)
            for key, value in availability_dict.items():
                if value is not None:
                    setattr(availability_db, key, value)
            session.add(availability_db)
            session.commit()
            session.refresh(availability_db)
            return availability_db
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Team availability with user ID {availability.team_id} and available from {availability.available_from} already exists")
        except Exception as e:
            session.rollback()
            raise e


# delete team availability
def delete_team_availability(availability: TeamAvailability):
    with Session(engine) as session:
        try:
            session.delete(availability)
            session.commit()
            return {"status": "deleted"}
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team availability with user ID {availability.team_id} and available from {availability.available_from} not deleted")


# delete all team availabilities
def delete_all_team_availabilities(team: Team):
    with Session(engine) as session:
        try:
            statement = select(TeamAvailability).where(
                TeamAvailability.team_id == team.team_id)
            availabilities = session.exec(statement).all()
            if not availabilities:
                raise HTTPException(
                    status_code=404, detail=f"Team availabilities not found")
            session.delete(availabilities)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team availabilities not deleted")


################################ team section ###############################################################################################
# get all teams
def all_teams():
    with Session(engine) as session:
        return session.exec(select(Team)).all()


# get team
def get_team(team_name: str):
    with Session(engine) as session:
        statement = select(Team).where(Team.team_name == team_name)
        team = session.exec(statement).first()
        if not team:
            return None
        return team


# get team by id
def get_team_by_id(team_id: int):
    with Session(engine) as session:
        statement = select(Team).where(Team.team_id == team_id)
        team = session.exec(statement).first()
        if not team:
            return None
        return team


# create team
def create_team(new_team: Team):
    with Session(engine) as session:
        try:
            db_team = Team.from_orm(new_team)
            session.add(db_team)
            session.commit()
            session.refresh(db_team)
            if not db_team:
                raise HTTPException(
                    status_code=404, detail=f"Team with name {new_team.team_name} not saved")
            return db_team
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Team with name {new_team.team_name} already exists")
        except Exception as e:
            session.rollback()
            raise e


# get team rating
def get_team_rating(team: Team):
    with Session(engine) as session:
        statement = select(Team).where(Team.team_id == team.team_id)
        db_team = session.exec(statement).first()
        if not team:
            return None
        return {db_team.total_rating_count, db_team.total_rating}


# get teams by rating
def get_teams_by_rating(rating: int):
    with Session(engine) as session:
        statement = select(Team).where(Team.total_rating >= rating)
        teams = session.exec(statement).all()
        if not teams:
            raise HTTPException(
                status_code=404, detail=f"No teams found with rating {rating}")


# update team's rating from matches
def update_team_rating(team: Team):
    with Session(engine) as session:
        statement = select(MatchTeamLink).where(
            MatchTeamLink.team_id == team.team_id)
        team_matches = session.exec(statement).all()
        if not team_matches:
            return None
        for team_match in team_matches:
            total_rating_count = team.total_rating_count + 1
            total_rating = team.total_rating * team.total_rating_count
            total_rating += team_match.team_rating
            total_rating_average = total_rating / total_rating_count
            total_rating_average = round(total_rating_average, 2)
            total_matches = team.total_matches + 1
            goals_scored_count = team.total_goals_scored + team_match.team_goals_scored
            total_goals_scored = goals_scored_count + total_goals_scored
            goals_conceded_count = team.total_goals_conceded + team_match.team_goals_conceded
            total_goals_conceded = goals_conceded_count + total_goals_conceded
            yellow_cards_count = team.total_yellow_cards + team_match.team_yellow_cards
            total_yellow_cards = yellow_cards_count + total_yellow_cards
            red_cards_count = team.total_red_cards + team_match.team_red_cards
            total_red_cards = red_cards_count + total_red_cards
            penalties_scored_count = team.total_penalties_scored + \
                team_match.team_penalties_scored
            penalties_scored_total = penalties_scored_count + penalties_scored_total
            penalties_missed_count = team.total_penalties_missed + \
                team_match.team_penalties_missed
            penalties_missed_total = penalties_missed_count + penalties_missed_total

            team.total_rating_count = total_rating_count
            team.total_rating = total_rating_average
            team.total_matches = total_matches
            team.total_goals_scored = total_goals_scored
            team.total_goals_conceded = total_goals_conceded
            team.total_yellow_cards = total_yellow_cards
            team.total_red_cards = total_red_cards
            team.total_penalties_scored = penalties_scored_total
            team.total_penalties_missed = penalties_missed_total

            session.add(team)
            session.commit()
            session.refresh(team)
            return team


# get team home stadium
def get_home_stadium(team: Team):
    with Session(engine) as session:
        statement = select(Stadium).where(
            Stadium.stadium_id == team.home_stadium_id)
        stadium = session.exec(statement).first()
        if not stadium:
            return None
        return stadium


# update team
def update_team(team_update: TeamUpdate):
    with Session(engine) as session:
        try:
            team_db = get_team(team_update.team_name)
            if not team_db:
                raise HTTPException(
                    status_code=404, detail=f"Team with name {team_update.team_name} not found")
            team_dict = team_update.dict(exclude_unset=True)
            for key, value in team_dict.items():
                if value is not None:
                    setattr(team_db, key, value)
            if 'captain_id' in team_dict and team_dict['captain_id'] is None:
                team_db.captain_id = None
            session.add(team_db)
            session.commit()
            session.refresh(team_db)
            return team_db
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Team with name {team_update.team_name} did not update!")
        except Exception as e:
            session.rollback()
            raise e


# delete team
def delete_team(team_name: str):
    delete_team = get_team(team_name)
    with Session(engine) as session:
        try:
            session.delete(delete_team)
            session.commit()
            return {f"Team with name: {team_name} has been deleted successfully"}
        except:
            session.rollback()
        raise HTTPException(
            status_code=404, detail=f"{team_name} not found")


################################# Stadium Referees Section #######################################################################################################
# get all stadium referees
def all_stadiums_referees():
    with Session(engine) as session:
        return session.exec(select(StadiumRefereeLink)).all()


# get all referee stadiums
def get_referee_stadiums(referee: Referee):
    with Session(engine) as session:
        statement = select(StadiumRefereeLink).where(
            StadiumRefereeLink.referee_id == referee.referee_id)
        referee_stadiums = session.exec(statement).all()
        if not referee_stadiums:
            return None
        return referee_stadiums


# get all stadium referees
def get_stadium_referees(stadium: Stadium):
    with Session(engine) as session:
        statement = select(StadiumRefereeLink).where(
            StadiumRefereeLink.stadium_id == stadium.stadium_id)
        stadium_referees = session.exec(statement).all()
        if not stadium_referees:
            return None
        return stadium_referees


# get stadium referee
def get_stadium_referee(stadium_referee: StadiumRefereeLink):
    with Session(engine) as session:
        statement = select(StadiumRefereeLink).where(
            StadiumRefereeLink.stadium_id == stadium_referee.stadium_id).where(StadiumRefereeLink.referee_id == stadium_referee.referee_id)
        stadium_referee = session.exec(statement).first()
        if not stadium_referee:
            return None
        return stadium_referee


# add stadium referee
def add_stadium_referee(stadium_referee: StadiumRefereeLink):
    with Session(engine) as session:
        try:
            db_stadium_referee = StadiumRefereeLink.from_orm(
                StadiumRefereeLink(stadium_id=stadium_referee.stadium_id, referee_id=stadium_referee.referee_id))
            session.add(db_stadium_referee)
            session.commit()
            session.refresh(db_stadium_referee)
            return db_stadium_referee
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Referee with id {stadium_referee.referee_id} not added to stadium {stadium_referee.stadium_id}")


# remove stadium referee
def remove_stadium_referee(stadium_referee: StadiumRefereeLink):
    with Session(engine) as session:
        statement = select(StadiumRefereeLink).where(
            StadiumRefereeLink.stadium_id == stadium_referee.stadium_id).where(StadiumRefereeLink.referee_id == stadium_referee.referee_id)
        stadium_referee = session.exec(statement).first()
        if not stadium_referee:
            return None
        session.delete(stadium_referee)
        session.commit()
        return stadium_referee


# update stadium referee
def update_stadium_referee(stadium_referee: StadiumRefereeLink):
    with Session(engine) as session:
        try:
            statement = select(StadiumRefereeLink).where(StadiumRefereeLink.stadium_id == stadium_referee.stadium_id).where(
                StadiumRefereeLink.referee_id == stadium_referee.referee_id)
            db_stadium_referee = session.exec(statement).first()
            if not db_stadium_referee:
                raise HTTPException(
                    status_code=404, detail=f"Referee is not in stadium")
            stadium_referee_dict = stadium_referee.dict(exclude_unset=True)
            for key, value in stadium_referee_dict.items():
                if value is not None:
                    setattr(db_stadium_referee, key, value)
            session.add(db_stadium_referee)
            session.commit()
            session.refresh(db_stadium_referee)
            return db_stadium_referee
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Stadium referee not updated!")


################################# Stadium Coaches Section ##################################################################################################
# get all stadiums coaches
def all_stadiums_coaches():
    with Session(engine) as session:
        return session.exec(select(StadiumCoachLink)).all()


# get all coach stadiums
def get_coach_stadiums(coach: Coach):
    with Session(engine) as session:
        statement = select(StadiumCoachLink).where(
            StadiumCoachLink.coach_id == coach.coach_id)
        coach_stadiums = session.exec(statement).all()
        if not coach_stadiums:
            return None
        return coach_stadiums


# get all stadium coaches
def get_stadium_coaches(stadium: Stadium):
    with Session(engine) as session:
        statement = select(StadiumCoachLink).where(
            StadiumCoachLink.stadium_id == stadium.stadium_id)
        stadium_coaches = session.exec(statement).all()
        if not stadium_coaches:
            return None
        return stadium_coaches


# get stadium coach
def get_stadium_coach(stadium_coach: StadiumCoachLink):
    with Session(engine) as session:
        statement = select(StadiumCoachLink).where(
            StadiumCoachLink.stadium_id == stadium_coach.stadium_id).where(StadiumCoachLink.coach_id == stadium_coach.coach_id)
        stadium_coach = session.exec(statement).first()
        if not stadium_coach:
            return None
        return stadium_coach


# add stadium coach
def add_stadium_coach(stadium_coach: StadiumCoachLink):
    with Session(engine) as session:
        try:
            db_stadium_coach = StadiumCoachLink.from_orm(
                StadiumCoachLink(stadium_id=stadium_coach.stadium_id, coach_id=stadium_coach.coach_id))
            session.add(db_stadium_coach)
            session.commit()
            session.refresh(db_stadium_coach)
            return db_stadium_coach
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Coach with id {stadium_coach.coach_id} not added to stadium {stadium_coach.stadium_id}")


# remove stadium coach
def remove_stadium_coach(stadium_coach: StadiumCoachLink):
    with Session(engine) as session:
        statement = select(StadiumCoachLink).where(
            StadiumCoachLink.stadium_id == stadium_coach.stadium_id).where(StadiumCoachLink.coach_id == stadium_coach.coach_id)
        stadium_coach = session.exec(statement).first()
        if not stadium_coach:
            return None
        session.delete(stadium_coach)
        session.commit()
        return stadium_coach


# update stadium coach
def update_stadium_coach(stadium_coach: StadiumCoachLink):
    with Session(engine) as session:
        try:
            statement = select(StadiumCoachLink).where(StadiumCoachLink.stadium_id == stadium_coach.stadium_id).where(
                StadiumCoachLink.coach_id == stadium_coach.coach_id)
            db_stadium_coach = session.exec(statement).first()
            if not db_stadium_coach:
                raise HTTPException(
                    status_code=404, detail=f"Coach is not in stadium")
            stadium_coach_dict = stadium_coach.dict(exclude_unset=True)
            for key, value in stadium_coach_dict.items():
                if value is not None:
                    setattr(db_stadium_coach, key, value)
            session.add(db_stadium_coach)
            session.commit()
            session.refresh(db_stadium_coach)
            return db_stadium_coach
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Stadium coach not updated!")


################################# Match Coaches Section #####################################################################################################
# get all matches coaches
def all_matches_coaches():
    with Session(engine) as session:
        return session.exec(select(MatchCoachLink)).all()


# get all coach matches
def get_coach_matches(coach: Coach):
    with Session(engine) as session:
        statement = select(MatchCoachLink).where(
            MatchCoachLink.coach_id == coach.coach_id)
        coach_matches = session.exec(statement).all()
        if not coach_matches:
            return None
        return coach_matches


# get all match coaches
def get_match_coaches(match: Match):
    with Session(engine) as session:
        statement = select(MatchCoachLink).where(
            MatchCoachLink.match_id == match.match_id)
        match_coaches = session.exec(statement).all()
        if not match_coaches:
            return None
        return match_coaches


# get match coach
def get_match_coach(match_coach: MatchCoachLink):
    with Session(engine) as session:
        statement = select(MatchCoachLink).where(
            MatchCoachLink.match_id == match_coach.match_id).where(MatchCoachLink.coach_id == match_coach.coach_id)
        match_coach = session.exec(statement).first()
        if not match_coach:
            return None
        return match_coach


# add match coach
def add_match_coach(match_coach: MatchCoachLink):
    with Session(engine) as session:
        try:
            db_match_coach = MatchCoachLink.from_orm(
                MatchCoachLink(match_id=match_coach.match_id, coach_id=match_coach.coach_id))
            session.add(db_match_coach)
            session.commit()
            session.refresh(db_match_coach)
            return db_match_coach
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Coach with id {match_coach.coach_id} not added to match {match_coach.match_id}")


# remove match coach
def remove_match_coach(match_coach: MatchCoachLink):
    with Session(engine) as session:
        statement = select(MatchCoachLink).where(
            MatchCoachLink.match_id == match_coach.match_id).where(MatchCoachLink.coach_id == match_coach.coach_id)
        match_coach = session.exec(statement).first()
        if not match_coach:
            return None
        session.delete(match_coach)
        session.commit()
        return match_coach


# update match coach
def update_match_coach(match_coach: MatchCoachLink):
    with Session(engine) as session:
        try:
            statement = select(MatchCoachLink).where(MatchCoachLink.match_id == match_coach.match_id).where(
                MatchCoachLink.coach_id == match_coach.coach_id)
            db_match_coach = session.exec(statement).first()
            if not db_match_coach:
                raise HTTPException(
                    status_code=404, detail=f"Coach is not in match")
            match_coach_dict = match_coach.dict(exclude_unset=True)
            for key, value in match_coach_dict.items():
                if value is not None:
                    setattr(db_match_coach, key, value)
            session.add(db_match_coach)
            session.commit()
            session.refresh(db_match_coach)
            return db_match_coach
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match coach not updated!")


################################# Team Coaches Section #####################################################################################################
# get all teams coaches
def all_teams_coaches():
    with Session(engine) as session:
        return session.exec(select(TeamCoachLink)).all()


# get all coach teams
def get_coach_teams(coach: Coach):
    with Session(engine) as session:
        statement = select(TeamCoachLink).where(
            TeamCoachLink.coach_id == coach.coach_id)
        coach_teames = session.exec(statement).all()
        if not coach_teames:
            return None
        return coach_teames


# get all team coaches
def get_team_coaches(team: Team):
    with Session(engine) as session:
        statement = select(TeamCoachLink).where(
            TeamCoachLink.team_id == team.team_id)
        team_coaches = session.exec(statement).all()
        if not team_coaches:
            return None
        return team_coaches


# get team coach
def get_team_coach(team_coach: TeamCoachLink):
    with Session(engine) as session:
        statement = select(TeamCoachLink).where(
            TeamCoachLink.team_id == team_coach.team_id).where(TeamCoachLink.coach_id == team_coach.coach_id)
        team_coach = session.exec(statement).first()
        if not team_coach:
            return None
        return team_coach


# add team coach
def add_team_coach(team_coach: TeamCoachLink):
    with Session(engine) as session:
        try:
            db_team_coach = TeamCoachLink.from_orm(
                TeamCoachLink(team_id=team_coach.team_id, coach_id=team_coach.coach_id))
            session.add(db_team_coach)
            session.commit()
            session.refresh(db_team_coach)
            return db_team_coach
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Coach with id {team_coach.coach_id} not added to team {team_coach.team_id}")


# remove team coach
def remove_team_coach(team_coach: TeamCoachLink):
    with Session(engine) as session:
        statement = select(TeamCoachLink).where(
            TeamCoachLink.team_id == team_coach.team_id).where(TeamCoachLink.coach_id == team_coach.coach_id)
        team_coach = session.exec(statement).first()
        if not team_coach:
            return None
        session.delete(team_coach)
        session.commit()
        return team_coach


# update team coach
def update_team_coach(team_coach: TeamCoachLink):
    with Session(engine) as session:
        try:
            statement = select(TeamCoachLink).where(TeamCoachLink.team_id == team_coach.team_id).where(
                TeamCoachLink.coach_id == team_coach.coach_id)
            db_team_coach = session.exec(statement).first()
            if not db_team_coach:
                raise HTTPException(
                    status_code=404, detail=f"Coach is not in team")
            team_coach_dict = team_coach.dict(exclude_unset=True)
            for key, value in team_coach_dict.items():
                if value is not None:
                    setattr(db_team_coach, key, value)
            session.add(db_team_coach)
            session.commit()
            session.refresh(db_team_coach)
            return db_team_coach
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Team coach not updated!")


# rate team coach
def rate_team_coach(team_coach: TeamCoachLink):
    with Session(engine) as session:
        statement = select(TeamCoachLink).where(
            TeamCoachLink.coach_id == team_coach.coach_id)
        db_team_coach = session.exec(statement).first()
        if not team_coach:
            return None
        db_team_coach.team_coach_rating_count = db_team_coach.team_coach_rating_count + 1
        total_rating = db_team_coach.team_coach_rating * \
            db_team_coach.team_coach_rating_count
        total_rating += team_coach.team_coach_rating
        total_rating_average = total_rating / db_team_coach.team_coach_rating_count
        db_team_coach.team_coach_rating = round(total_rating_average, 2)
        session.add(db_team_coach)
        session.commit()
        session.refresh(db_team_coach)
        return db_team_coach


# get team coach rating
def get_team_coach_rating(team_coach: TeamCoachLink):
    with Session(engine) as session:
        statement = select(TeamCoachLink).where(
            TeamCoachLink.coach_id == team_coach.coach_id)
        db_team_coach = session.exec(statement).first()
        if not db_team_coach:
            return None
        return {"team_coach_rating_count": db_team_coach.team_coach_rating_count, "team_coach_rating": db_team_coach.team_coach_rating}


################################# Player Coaches Section #####################################################################################################
# get all players coaches
def all_players_coaches():
    with Session(engine) as session:
        return session.exec(select(PlayerCoachLink)).all()


# get all coach players
def get_coach_players(coach: Coach):
    with Session(engine) as session:
        statement = select(PlayerCoachLink).where(
            PlayerCoachLink.coach_id == coach.coach_id)
        coach_playeres = session.exec(statement).all()
        if not coach_playeres:
            return None
        return coach_playeres


# get all player coaches
def get_player_coach(player: Player):
    with Session(engine) as session:
        statement = select(PlayerCoachLink).where(
            PlayerCoachLink.player_id == player.player_id)
        player_coach = session.exec(statement).first()
        if not player_coach:
            return None
        return player_coach


# add player coach
def add_player_coach(player_coach: PlayerCoachLink):
    with Session(engine) as session:
        try:
            db_player_coach = PlayerCoachLink.from_orm(
                PlayerCoachLink(player_id=player_coach.player_id, coach_id=player_coach.coach_id))
            session.add(db_player_coach)
            session.commit()
            session.refresh(db_player_coach)
            return db_player_coach
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Coach with id {player_coach.coach_id} not added to player {player_coach.player_id}")


# remove player coach
def remove_player_coach(player_coach: PlayerCoachLink):
    with Session(engine) as session:
        statement = select(PlayerCoachLink).where(
            PlayerCoachLink.player_id == player_coach.player_id).where(PlayerCoachLink.coach_id == player_coach.coach_id)
        player_coach = session.exec(statement).first()
        if not player_coach:
            return None
        session.delete(player_coach)
        session.commit()
        return player_coach


# update player coach
def update_player_coach(player_coach: PlayerCoachLink):
    with Session(engine) as session:
        try:
            statement = select(PlayerCoachLink).where(PlayerCoachLink.player_id == player_coach.player_id).where(
                PlayerCoachLink.coach_id == player_coach.coach_id)
            db_player_coach = session.exec(statement).first()
            if not db_player_coach:
                raise HTTPException(
                    status_code=404, detail=f"Coach is not in player")
            player_coach_dict = player_coach.dict(exclude_unset=True)
            for key, value in player_coach_dict.items():
                if value is not None:
                    setattr(db_player_coach, key, value)
            session.add(db_player_coach)
            session.commit()
            session.refresh(db_player_coach)
            return db_player_coach
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Player coach not updated!")


# rate player coach
def player_coach_rating(player_coach: PlayerCoachLink):
    with Session(engine) as session:
        statement = select(PlayerCoachLink).where(
            PlayerCoachLink.coach_id == player_coach.coach_id)
        db_player_coach = session.exec(statement).first()
        if not player_coach:
            return None
        db_player_coach.player_coach_rating_count += 1
        total_rating = db_player_coach.player_coach_rating * \
            db_player_coach.player_coach_rating_count
        total_rating += player_coach.player_coach_rating
        total_rating_average = total_rating / db_player_coach.player_coach_rating_count
        db_player_coach.player_coach_rating = round(total_rating_average, 2)
        session.add(db_player_coach)
        session.commit()
        session.refresh(db_player_coach)
        return db_player_coach


# get player coach rating
def get_player_coach_rating(player_coach: PlayerCoachLink):
    with Session(engine) as session:
        statement = select(PlayerCoachLink).where(
            PlayerCoachLink.coach_id == player_coach.coach_id)
        db_player_coach = session.exec(statement).first()
        if not db_player_coach:
            return None
        return {"player_coach_rating_count": db_player_coach.player_coach_rating_count, "player_coach_rating": db_player_coach.player_coach_rating}


############################################# Coach section ##################################################################################
# get all coaches
def all_coaches():
    with Session(engine) as session:
        return session.exec(select(Coach)).all()


# create coach
def create_coach(new_coach: Coach):
    with Session(engine) as session:
        try:
            db_coach = Coach.from_orm(new_coach)
            session.add(db_coach)
            session.commit()
            session.refresh(db_coach)
            if not db_coach:
                raise HTTPException(
                    status_code=404, detail=f"Coach with username {new_coach.username} not saved")
            update_coach_id(new_coach.user_id, db_coach.coach_id)
            return db_coach
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Coach with username {new_coach.username} already exists")
        except Exception as e:
            session.rollback()
            raise e


# get coach
def get_coach(username: str):
    with Session(engine) as session:
        statement = select(Coach).where(Coach.username == username)
        coach = session.exec(statement).first()
        if not coach:
            return None
        return coach


# get coach by id
def get_coach_by_id(coach_id: int):
    with Session(engine) as session:
        statement = select(Coach).where(Coach.coach_id == coach_id)
        coach = session.exec(statement).first()
        if not coach:
            return None
        return coach


# update coach
def update_coach(coach: CoachUpdate):
    with Session(engine) as session:
        try:
            coach_db = get_coach(coach.username)
            if not coach_db:
                raise HTTPException(
                    status_code=404, detail=f"Coach with username {coach.username} not found")
            coach_dict = coach.dict(exclude_unset=True)
            for key, value in coach_dict.items():
                if value is not None:
                    setattr(coach_db, key, value)
            session.add(coach_db)
            session.commit()
            session.refresh(coach_db)
            return coach_db
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Coach with username {coach.username} did not update!")


# update coach_id in user table
def update_coach_id(user_id: int, coach_id: int | None = None):
    with Session(engine) as session:
        statement = select(User).where(
            User.id == user_id)
        results = session.exec(statement)
        user = results.first()
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User not found")
        user.coach_id = coach_id
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


# update coach rating in the database
def update_coach_rating(coach: Coach):
    with Session(engine) as session:
        statement = select(Coach).where(
            Coach.coach_id == coach.coach_id)
        results = session.exec(statement)
        db_coach = results.first()
        if not db_coach:
            raise HTTPException(
                status_code=404, detail=f"Coach with username {coach.username} not found"
            )
        # add coach players rating and counts
        coach_players = get_coach_players(db_coach)
        for coach_player in coach_players:
            db_coach.total_rating_count = db_coach.total_rating_count + \
                coach_player.player_coach_rating_count
            total_rating = coach_player.player_coach_rating * db_coach.total_rating_count
            total_rating += db_coach.total_rating
            total_rating_average = total_rating / db_coach.total_rating_count
            db_coach.total_rating = round(total_rating_average, 2)
            session.add(db_coach)
            session.commit()
            session.refresh(db_coach)
    # add coach teams rating and counts
    with Session(engine) as session:
        coach_teams = get_coach_teams(db_coach)
        for coach_team in coach_teams:
            db_coach.total_rating_count = db_coach.total_rating_count + \
                coach_team.team_coach_rating_count
            total_rating = coach_team.team_coach_rating * db_coach.total_rating_count
            total_rating += db_coach.total_rating
            total_rating_average = total_rating / db_coach.total_rating_count
            db_coach.total_rating = round(total_rating_average, 2)
            session.add(db_coach)
            session.commit()
            session.refresh(db_coach)
            return db_coach


# get coach total rating
def get_coach_total_rating(coach: Coach):
    with Session(engine) as session:
        statement = select(Coach).where(
            Coach.coach_id == coach.coach_id)
        results = session.exec(statement)
        db_coach = results.first()
        if not db_coach:
            raise HTTPException(
                status_code=404, detail=f"Coach with username {coach.username} not found")
        return {"total_rating_count": db_coach.total_rating_count, "total_rating": db_coach.total_rating}


# get coaches by rating
def get_coaches_by_rating(rating: int):
    with Session(engine) as session:
        statement = select(Coach).where(Coach.total_rating >= rating)
        coaches = session.exec(statement).all()
        if not coaches:
            raise HTTPException(
                status_code=404, detail=f"No coaches found with rating {rating}")
        return coaches


# get coaches in a radius
def get_coaches_in_radius(longitude: float, latitude: float, radius: float):
    search_area = get_search_area(
        latitude=latitude, longitude=longitude, radius=radius)
    with Session(engine) as session:
        # Query players within the specified radius
        coaches = session.exec(select(Coach).where(
            Coach.coach_longitude >= search_area['min_longitude'],
            Coach.coach_longitude <= search_area['max_longitude'],
            Coach.coach_latitude >= search_area['min_latitude'],
            Coach.coach_latitude <= search_area['max_latitude']
        )).all()

        if not coaches:
            raise HTTPException(
                status_code=404, detail=f"No coaches found within {radius} km radius")
        return coaches


# get coaches by rating and location radius
def get_coaches_by_rating_radius(coach: Coach, rating: int, radius: float):
    with Session(engine) as session:
        # get coaches within the specified radius
        coaches = get_coaches_in_radius(coach, radius)
        if not coaches:
            raise HTTPException(
                status_code=404, detail=f"No coaches found within {radius} km radius")
        # filter coaches by rating
        found_coaches = list(
            filter(lambda found_coach: found_coach.total_rating >= rating, coaches))
        if not found_coaches:
            raise HTTPException(
                status_code=404, detail=f"No coaches found with at least a rating of {rating} and within {radius} km radius")
        return found_coaches


# get coaches by home stadium
def get_coaches_by_stadium(stadium_id: int):
    with Session(engine) as session:
        return session.exec(select(StadiumCoachLink).where(StadiumCoachLink.stadium_id == stadium_id).where(StadiumCoachLink.is_home_stadium == True)).all()


# delete coach
def delete_coach(coach: Coach):
    with Session(engine) as session:
        try:
            update_coach_id(coach.user_id, None)
            session.delete(coach)
            session.commit()
            return {"status": "deleted"}
        except:
            session.rollback()
        raise HTTPException(
            status_code=404, detail=f"{coach.username} not deleted!")


############################# Stadium section ##################################################################################
# get all stadiums
def all_stadiums():
    with Session(engine) as session:
        stadiums = session.exec(select(Stadium)).all()
        if not stadiums:
            return None
        return stadiums


# create stadium
def create_stadium(new_stadium: Stadium):
    with Session(engine) as session:
        try:
            db_stadium = Stadium(
                **new_stadium.dict()
            )
            session.add(db_stadium)
            session.commit()
            session.refresh(db_stadium)
            return db_stadium
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=404, detail=str(e))


# get stadium
def get_stadium(stadium_id: int):
    with Session(engine) as session:
        statement = select(Stadium).where(Stadium.stadium_id == stadium_id)
        stadium = session.exec(statement).first()
        if not stadium:
            return None
        return stadium


# get stadiums by stadium_name
def get_stadiums_by_name(stadium_name: str):
    with Session(engine) as session:
        statement = select(Stadium).where(Stadium.stadium_name == stadium_name)
        stadiums = session.exec(statement).all()
        if not stadiums:
            return None
        return stadiums


# get stadium by city from Google Places API
def get_google_city_stadiums(city: str):
    try:
        response = gmaps.places(
            query=f"terrains de proximité de football in {city}", type="football stadium")
        stadiums = response["results"]
        return stadiums
    except ApiError as e:
        return {"error": str(e)}


# format stadium info from Google Places API
def format_stadium_info(stadium_resp: dict):
    stadium_info = {
        "stadium_name": stadium_resp["name"],
        "google_place_id": stadium_resp["place_id"],
        "stadium_phone_number": stadium_resp.get("international_phone_number"),
        "stadium_address": stadium_resp.get("formatted_address"),
        "stadium_longitude": stadium_resp.get("geometry", {}).get("location", {}).get("lng"),
        "stadium_latitude": stadium_resp.get("geometry", {}).get("location", {}).get("lat"),
        "stadium_city": stadium_resp.get("plus_code", {}).get("compound_code"),
        "stadium_rating_total": stadium_resp.get("user_ratings_total"),
        "stadium_rating": stadium_resp.get("rating"),
        "google_image_reference": stadium_resp.get("photos", [{}])[0].get("photo_reference")
    }

    return stadium_info


# get stadium by place_id from Google Places API
def get_stadium_by_place_id(place_id: str):
    with Session(engine) as session:
        statement = select(Stadium).where(Stadium.google_place_id == place_id)
        stadium = session.exec(statement).first()
        if not stadium:
            return None
        return stadium


# get stadiums by city
def get_stadiums_by_city(city: str):
    with Session(engine) as session:
        statement = select(Stadium).where(Stadium.stadium_city == city)
        stadium = session.exec(statement).all()
        if not stadium:
            return None
        return stadium


# get all stadiums within a radius from current location
def get_stadiums_within_radius(longitude: float, latitude: float, radius: float):
    search_area = get_search_area(
        latitude=latitude, longitude=longitude, radius=radius)
    with Session(engine) as session:
        # Query stadiums within the specified radius
        stadiums = session.exec(select(Stadium).where(
            Stadium.stadium_longitude >= search_area["min_longitude"],
            Stadium.stadium_longitude <= search_area["max_longitude"],
            Stadium.stadium_latitude >= search_area["min_latitude"],
            Stadium.stadium_latitude <= search_area["max_latitude"]
        )).all()

        if not stadiums:
            raise HTTPException(
                status_code=404, detail=f"No stadiums found within {radius} km radius")
        return stadiums


# update stadium
def update_stadium(stadium: Stadium, stadium_update: StadiumUpdate):
    with Session(engine) as session:
        try:
            stadium_dict = stadium_update.dict(exclude_unset=True)
            for key, value in stadium_dict.items():
                if value is not None:
                    setattr(stadium, key, value)
            session.add(stadium)
            session.commit()
            session.refresh(stadium)
            return stadium
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Stadium with ID {stadium.stadium_id} not updated")


# delete stadium
def delete_stadium(stadium_id: int):
    delete_stadium = get_stadium(stadium_id)
    with Session(engine) as session:
        try:
            session.delete(delete_stadium)
            session.commit()
            return {f"Stadium with ID: {stadium_id} has been deleted successfully"}
        except:
            session.rollback()
        raise HTTPException(
            status_code=404, detail=f"{stadium_id} not found")


# get stadium matches
def get_stadium_matches(stadium: Stadium):
    with Session(engine) as session:
        statement = select(Match).where(Match.stadium_id == stadium.stadium_id)
        matches = session.exec(statement).all()
        if not matches:
            return None
        return matches


# get stadium home teams
def get_stadium_home_teams(stadium: Stadium):
    with Session(engine) as session:
        statement = select(Team).where(
            Team.home_stadium_id == stadium.stadium_id)
        teams = session.exec(statement).all()
        if not teams:
            return None
        return teams


############################ match section ##################################################################################
# get all matches
def get_matches():
    with Session(engine) as session:
        return session.exec(select(Match)).all()


# get all matches in a date
def get_all_matches_by_date(stadium_id: int, match_date: date):
    with Session(engine) as session:
        statement = select(Match).where(Match.stadium_id == stadium_id).where(
            Match.match_start_time.between(match_date, match_date + timedelta(days=1)))
        matches = session.exec(statement).all()
        if not matches:
            return None
        return matches


# get match
def get_match(match_id: int):
    with Session(engine) as session:
        statement = select(Match).where(Match.match_id == match_id)
        match = session.exec(statement).first()
        if not match:
            return None
        return match


# create match
def create_match(match: MatchCreate):
    with Session(engine) as session:
        try:
            new_match = Match(**match.dict())
            session.add(new_match)
            session.commit()
            session.refresh(new_match)
            return new_match
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match not created")


# assign match home team
def assign_match_home_team(match: Match, team: Team):
    with Session(engine) as session:
        try:
            statement = select(Match).where(Match.match_id == match.match_id)
            db_match = session.exec(statement).first()
            db_match.home_team_id = team.team_id
            db_match.home_team_name = team.team_name
            session.add(db_match)
            session.commit()
            session.refresh(db_match)
            return add_match_team(match=match, team=team, is_home_team=True)
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match with id {db_match.match_id} not updated")


# assign match away team
def assign_match_away_team(match: Match, team: Team):
    with Session(engine) as session:
        try:
            statement = select(Match).where(Match.match_id == match.match_id)
            db_match = session.exec(statement).first()
            db_match.away_team_id = team.team_id
            db_match.away_team_name = team.team_name
            session.add(db_match)
            session.commit()
            session.refresh(db_match)
            return add_match_team(match=match, team=team, is_home_team=False)
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match with id {match.match_id} not updated")


# remove match away team
def remove_match_away_team(match: Match):
    with Session(engine) as session:
        try:
            statement = select(Match).where(Match.match_id == match.match_id)
            db_match = session.exec(statement).first()
            db_match.away_team_id = None
            db_match.away_team_name = None
            session.add(db_match)
            session.commit()
            session.refresh(db_match)
            return remove_match_team(match=match, is_home_team=False)
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match with id {match.match_id} not updated")

# update match


def update_match(match_update: Match):
    with Session(engine) as session:
        try:
            statement = select(Match).where(
                Match.match_id == match_update.match_id)
            db_match = session.exec(statement).first()
            if not db_match:
                raise HTTPException(
                    status_code=404, detail=f"Match with id {match_update.match_id} not found")
            match_dict = match_update.dict(exclude_unset=True)
            for key, value in match_dict.items():
                if value is not None:
                    setattr(db_match, key, value)
            session.add(db_match)
            session.commit()
            session.refresh(db_match)
            return db_match
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match not updated!")


# delete match
def delete_match(match_id: int):
    delete_match = get_match(match_id)
    with Session(engine) as session:
        try:
            session.delete(delete_match)
            session.commit()
            return {f"Match with id: {match_id} has been deleted successfully"}
        except:
            session.rollback()
        raise HTTPException(
            status_code=404, detail=f"Match with id {match_id} not found")


############################ match score section ##################################################################################
# get all matches scores
def get_matches_scores():
    with Session(engine) as session:
        return session.exec(select(MatchScore)).all()


# get match score
def get_match_score(match_id: int):
    with Session(engine) as session:
        statement = select(MatchScore).where(MatchScore.match_id == match_id)
        match_score = session.exec(statement).first()
        if not match_score:
            return None
        return match_score


# new match score
def new_match_score(match: Match):
    with Session(engine) as session:
        try:
            new_match_score = MatchScore(match_id=match.match_id, home_team_id=match.home_team_id,
                                         home_team_name=match.home_team_name, away_team_id=match.away_team_id, away_team_name=match.away_team_name)
            session.add(new_match_score)
            session.commit()
            session.refresh(new_match_score)
            return new_match_score
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match score board not created!")


# update match score
def update_match_score(match_score: MatchScore):
    with Session(engine) as session:
        try:
            statement = select(MatchScore).where(
                MatchScore.match_id == match_score.match_id)
            db_match_score = session.exec(statement).first()
            match_score_dict = match_score.dict(exclude_unset=True)
            for key, value in match_score_dict.items():
                if value is not None:
                    setattr(db_match_score, key, value)
            session.add(db_match_score)
            session.commit()
            session.refresh(db_match_score)
            return db_match_score
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match score board not updated!")


# delete match score
def delete_match_score(match_id: int):
    delete_match_score = get_match_score(match_id)
    with Session(engine) as session:
        try:
            session.delete(delete_match_score)
            session.commit()
            return {f"Match score board with id: {match_id} has been deleted successfully"}
        except:
            session.rollback()
        raise HTTPException(
            status_code=404, detail=f"Match score board with id {match_id} not found")


# add a new match goal scored
def add_match_goal_scored(match: Match, match_team: MatchTeamLink, player_match: MatchPlayerLink):
    add_match_player_goal(player_match)
    scoring_team = match.home_team_id if match_team.is_home_team == True else match.away_team_id
    add_match_team_goal(match, scoring_team)
    conceded_team = match.away_team_id if match_team.is_home_team == True else match.home_team_id
    add_match_team_goal_conceded(match, conceded_team)
    with Session(engine) as session:
        try:
            statement = select(MatchScore).where(
                MatchScore.match_id == match.match_id)
            match_score = session.exec(statement).first()
            if not match_score:
                match_score = new_match_score(match)
            if match_team.is_home_team == True:
                match_score.home_team_goals_scored += 1
                match_score.away_team_goals_conceded += 1
            else:
                match_score.away_team_goals_scored += 1
                match_score.home_team_goals_conceded += 1
            session.add(match_score)
            session.commit()
            session.refresh(match_score)
            return match_score
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match score board not updated!")


# add a new match yellow card
def add_match_yellow_card(match: Match, match_team: MatchTeamLink, match_player: MatchPlayerLink):
    add_match_player_yellow_card(match_player)
    add_match_team_yellow_card(match_team)
    with Session(engine) as session:
        try:
            statement = select(MatchScore).where(
                MatchScore.match_id == match.match_id)
            match_score = session.exec(statement).first()
            if not match_score:
                match_score = new_match_score(match)
            if match_team.is_home_team == True:
                match_score.home_team_yellow_cards += 1
            else:
                match_score.away_team_yellow_cards += 1
            session.add(match_score)
            session.commit()
            session.refresh(match_score)
            return match_score
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match score board not updated!")


# add a new match red card
def add_match_red_card(match: Match, match_team: MatchTeamLink, match_player: MatchPlayerLink):
    add_match_player_red_card(match_player)
    add_match_team_red_card(match_team)
    with Session(engine) as session:
        try:
            statement = select(MatchScore).where(
                MatchScore.match_id == match.match_id)
            match_score = session.exec(statement).first()
            if not match_score:
                match_score = new_match_score(match)
            if match_team.is_home_team == True:
                match_score.home_team_red_cards += 1
            else:
                match_score.away_team_red_cards += 1
            session.add(match_score)
            session.commit()
            session.refresh(match_score)
            return match_score
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match score board not updated!")


# add a new match penalty
def add_match_penalty(match: Match, match_team: MatchTeamLink, match_player: MatchPlayerLink, penalty_scored: bool):
    add_match_player_penalty(match_player, penalty_scored)
    scoring_team = match.home_team_id if match_team.is_home_team == True else match.away_team_id
    add_match_team_penalty_scored(match, scoring_team)
    missed_team = match.away_team_id if match_team.is_home_team == True else match.home_team_id
    add_match_team_penalty_missed(match, missed_team)
    with Session(engine) as session:
        try:
            statement = select(MatchScore).where(
                MatchScore.match_id == match.match_id)
            match_score = session.exec(statement).first()
            if not match_score:
                match_score = new_match_score(match)
            if match_team.is_home_team == True and penalty_scored == True:
                match_score.home_team_penalties_scored += 1
                match_score.home_team_goals_scored += 1
            elif match_team.is_home_team == False and penalty_scored == True:
                match_score.away_team_penalties_scored += 1
                match_score.away_team_goals_scored += 1
            elif match_team.is_home_team == True and penalty_scored == False:
                match_score.home_team_penalties_missed += 1
            match_score.away_team_penalties_missed += 1
            session.add(match_score)
            session.commit()
            session.refresh(match_score)
            return match_score
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match score board not updated!")


# update match result
def update_match_result(home_team: MatchTeamLink, away_team: MatchTeamLink, match_score: MatchScore):
    with Session(engine) as session:
        try:
            if match_score.home_team_goals_scored > match_score.away_team_goals_scored:
                match_score.winner_team = match_score.home_team_name
                match_score.loser_team = match_score.away_team_name
                match_score.draw_match = False
                home_team.match_result = "W"
                away_team.match_result = "L"
            elif match_score.home_team_goals_scored < match_score.away_team_goals_scored:
                match_score.winner_team = match_score.away_team_name
                match_score.loser_team = match_score.home_team_name
                match_score.draw_match = False
                home_team.match_result = "L"
                away_team.match_result = "W"
            match_score.draw_match = True
            home_team.match_result = "D"
            away_team.match_result = "D"
            session.add(match_score)
            session.add(home_team)
            session.add(away_team)
            session.commit()
            session.refresh(match_score)
            session.refresh(home_team)
            session.refresh(away_team)
            return match_score
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match score board not updated!")


################################## referee section ##################################################################################
# get all referees
def all_referees():
    with Session(engine) as session:
        return session.exec(select(Referee)).all()


# update referee_id in user table
def update_referee_id(user_id: int, referee_id: int | None = None):
    with Session(engine) as session:
        statement = select(User).where(
            User.id == user_id)
        results = session.exec(statement)
        user = results.first()
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with user ID: {user_id} not found")
        user.referee_id = referee_id
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


# get referee
def get_referee(username: str):
    with Session(engine) as session:
        statement = select(Referee).where(Referee.username == username)
        referee = session.exec(statement).first()
        if not referee:
            return None
        return referee


# create referee
def create_referee(new_referee: RefereeCreate):
    with Session(engine) as session:
        try:
            db_referee = Referee.from_orm(new_referee)
            session.add(db_referee)
            session.commit()
            session.refresh(db_referee)
            if not db_referee:
                raise HTTPException(
                    status_code=404, detail=f"Referee with username {new_referee.username} not saved!")
            update_referee_id(db_referee.user_id, db_referee.referee_id)
            return db_referee
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Referee with username {new_referee.username} already exists")
        except Exception as e:
            session.rollback()
            raise e


# get referees in a radius
def get_referees_in_radius(longitude: float, latitude: float, radius: float):
    search_area = get_search_area(
        latitude=latitude, longitude=longitude, radius=radius)
    with Session(engine) as session:
        # Query referees within the specified radius
        referees = session.exec(select(Referee).where(
            Referee.referee_longitude >= search_area["min_longitude"],
            Referee.referee_longitude <= search_area["max_longitude"],
            Referee.referee_latitude >= search_area["min_latitude"],
            Referee.referee_latitude <= search_area["max_latitude"]
        )).all()

        if not referees:
            raise HTTPException(
                status_code=404, detail=f"No referees found within {radius} km radius")
        return referees


# update referee
def update_referee(referee: RefereeUpdate):
    with Session(engine) as session:
        try:
            statement = select(Referee).where(
                Referee.username == referee.username)
            results = session.exec(statement)
            db_referee = results.first()
            if not db_referee:
                raise HTTPException(
                    status_code=404, detail=f"Referee with username {referee.username} not found")
            for var, value in vars(referee).items():
                if value is not None:
                    setattr(db_referee, var, value)
            session.add(db_referee)
            session.commit()
            session.refresh(db_referee)
            return db_referee
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Referee with username {referee.username} not updated!")


# delete referee
def delete_referee(referee: Referee):
    update_referee_id(referee.user_id, None)
    with Session(engine) as session:
        try:
            session.delete(referee)
            session.commit()
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Referee with username {referee.username} not deleted")
        return {"status": "deleted"}


#################### Match Referee Section ##############################################################
# get referee matches
def get_referee_matches(referee_id: int):
    with Session(engine) as session:
        statement = select(Match).where(Match.referee_id == referee_id)
        matches = session.exec(statement).all()
        if not matches:
            return None
        return matches


# assign match referee
def assign_match_referee(match_id: int, referee_id: int):
    with Session(engine) as session:
        try:
            statement = select(Match).where(Match.match_id == match_id)
            match_update = session.exec(statement).first()
            match_update.referee_id = referee_id
            session.commit()
            return match_update
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match with id {match_id} not updated")


# remove match referee
def remove_match_referee(match: Match):
    with Session(engine) as session:
        try:
            statement = select(Match).where(Match.match_id == match.match_id)
            match_update = session.exec(statement).first()
            match_update.referee_id = None
            session.commit()
            return match_update
        except:
            session.rollback()
            raise HTTPException(
                status_code=404, detail=f"Match with id {match.match_id} not updated")


##################### Referee Ratings Section ##################################################################
# update referee rating in the database
def update_referee_rating(referee: Referee):
    with Session(engine) as session:
        try:
            statement = select(Referee).where(
                Referee.referee_id == referee.referee_id)
            results = session.exec(statement)
            db_referee = results.first()
            if not db_referee:
                raise HTTPException(
                    status_code=404, detail=f"Referee with username {referee.username} not found"
                )
            # add referee matches rating and counts
            referee_matches = get_referee_matches(db_referee)
            for match in referee_matches:
                db_referee.total_rating_count += 1
                total_rating = db_referee.total_rating * db_referee.total_rating_count
                total_rating += db_referee.total_rating
                total_rating_average = total_rating / db_referee.total_rating_count
                db_referee.total_rating = round(total_rating_average, 2)
                session.add(db_referee)
                session.commit()
                session.refresh(db_referee)
            return db_referee

        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Referee {referee.username} ratings did not update!")


# get referees by rating
def get_referees_by_rating(rating: int):
    with Session(engine) as session:
        statement = select(Referee).where(Referee.total_rating >= rating)
        referees = session.exec(statement).all()
        if not referees:
            raise HTTPException(
                status_code=404, detail=f"No referees found with rating {rating}")
        return referees


########################## Booking section #############################################################
# get number of available pitches based on start and end time
def get_stadium_available_pitches(stadium: Stadium, start_time: datetime, duration: int):
    # get end time
    end_time = start_time + timedelta(minutes=duration)
    # get all matches in stadium
    matches = get_stadium_matches(stadium)
    if not matches:
        return stadium.number_of_pitches
    # get stadium available pitches
    for match in matches:
        match_end_time = match.match_start_time + \
            timedelta(minutes=match.match_duration)
        if start_time <= match.match_start_time <= end_time or start_time <= match_end_time <= end_time:
            available_pitches = stadium.number_of_pitches - 1
        return stadium.number_of_pitches
    return available_pitches
