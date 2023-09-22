from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from datetime import timedelta
from pydantic import EmailStr
from pathlib import Path
from .routers import users, players, managers, coaches, teams, stadiums, matches, referees
from .internal import superuser, users_admin, coaches_admin, managers_admin, players_admin, teams_admin, stadiums_admin, matches_admin, referees_admin, match_manager_admin, match_players_admin, match_referee_admin, match_referee_admin, match_referee_admin, match_teams_admin, player_coach_admin, stadium_coaches_admin, stadium_matches_admin, stadium_players_admin, stadium_referees_admin, stadium_teams_admin, team_coach_admin, team_manager_admin
from .models import UserRead, Token, UserCreate, User, UserUpdate
from .database import create_db_and_tables, disconnect_db
from .database import pg_engine as engine
from .dependencies import create_access_token, create_email_validation, send_validation_email, update_email_validation, get_email_validation, generate_validation_code, check_validation_code, authenticate_user, create_user, get_user, get_user_by_email, get_password_hash, update_user
from dotenv import load_dotenv
import os
load_dotenv()


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


def create_surperuser_accout():
    # hash the superuser password
    hashed_password = os.environ['FIRST_SUPERUSER_PASSWORD'] = get_password_hash(
        os.getenv('FIRST_SUPERUSER_PASSWORD'))
    # check if superuser exists and create it if not
    if not get_user(os.getenv('FIRST_SUPERUSER')):
        superuser = User(username=os.getenv('FIRST_SUPERUSER'), hashed_password=hashed_password,
                         email=os.getenv('FIRST_SUPERUSER_EMAIL'), mobile=os.getenv('FIRST_SUPERUSER_MOBILE'), first_name=os.getenv("FIRST_SUPERUSER_FIRST_NAME"), last_name=os.getenv('FIRST_SUPERUSER_LAST_NAME'), disabled=False, is_superuser=True, is_admin=True, email_validation=True, mobile_validation=True)
        create_user(superuser)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create Database and tables
    create_db_and_tables(engine)
    # create superuser account
    create_surperuser_accout()
    yield
    # disconnect Database
    disconnect_db(engine)


app = FastAPI(title="Team Up",
              description="Team Up API",
              version="0.1.0",
              lifespan=lifespan,
              generate_unique_id_function=custom_generate_unique_id
              )


internal = FastAPI(title="Team Up Admin",
                   description="Team Up Admin API",
                   version="0.1.0",
                   )


BASE_PATH = Path(__file__).resolve().parent
app.mount("/public", StaticFiles(directory='public'), name="public")
app.mount("/internal", internal, name="internal")


app.include_router(users.users_router)
app.include_router(players.players_router)
app.include_router(stadiums.stadiums_router)

app.include_router(managers.managers_router)
app.include_router(coaches.coaches_router)
app.include_router(teams.teams_router)
app.include_router(referees.referees_router)
app.include_router(matches.matches_router)
app.include_router(player_coach_admin.player_coach_router)
app.include_router(team_manager_admin.team_manager_router)
app.include_router(team_coach_admin.team_coach_router)
app.include_router(stadium_teams_admin.stadium_teams_router)
app.include_router(stadium_players_admin.stadium_players_router)
app.include_router(stadium_matches_admin.stadium_matches_router)
app.include_router(stadium_coaches_admin.stadium_coaches_router)
app.include_router(stadium_referees_admin.stadium_referees_router)
app.include_router(match_manager_admin.match_manager_router)
app.include_router(match_teams_admin.match_teams_router)
app.include_router(match_players_admin.match_players_router)
app.include_router(match_referee_admin.match_referee_router)


internal.include_router(superuser.superuser_router)
internal.include_router(users_admin.users_admin_router)
internal.include_router(players_admin.players_admin_router)
internal.include_router(stadiums_admin.stadiums_admin_router)
internal.include_router(managers_admin.managers_admin_router)
internal.include_router(referees_admin.referees_admin_router)
internal.include_router(coaches_admin.coaches_admin_router)
internal.include_router(teams_admin.teams_admin_router)
internal.include_router(matches_admin.matches_admin_router)


ALLOWED_ORIGINS = [
    "https://localhost:5173",
    "http://localhost:5173",
    "http://localhost:8501/",
    "http://localhost:5432/",
    "https://localhost:5432/",
    "http://localhost:8000/",
    "https://localhost:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict, tags=["Root"])
async def get_root():
    return {"message": "This is the root of the API"}


@app.post("/token", response_model=Token, tags=["Login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(days=7)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@internal.post("/token", response_model=Token, tags=["Login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(days=1)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/new_user", response_model=UserRead, tags=["Register"])
async def new_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password, email=user.email,
                    mobile=user.mobile, first_name=user.first_name, last_name=user.last_name, date_of_birth=user.date_of_birth, disabled=True)
    user = create_user(new_user)
    validation = create_email_validation(user)
    send_validation_email(validation)
    return user


@app.post("/new_social_registration", response_model=UserRead, tags=["Register"])
async def new_social_registration(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password,
                    mobile=user.mobile, first_name=user.first_name, last_name=user.last_name, user_photo=user.user_photo, date_of_birth=user.date_of_birth, email_validation=True, disabled=False)
    user = create_user(new_user)
    return user


# Update my email validation
@app.patch("/generate_new_email_validation/{email}", response_model=dict, tags=["Register"])
async def generate_new_email_validation(email: EmailStr):
    validation = get_email_validation(email)
    if validation:
        validation.email_validation_code = generate_validation_code()
        validation_update = update_email_validation(validation)
        send_validation_email(validation_update)
        return {"message": "New email validation code sent"}
    else:
        user = get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=400, detail="Email is not registered")
        validation = create_email_validation(user)
        send_validation_email(validation)
        return {"message": "New email validation code sent"}


# Validate my email
@app.patch("/validate_email/{email}/{validation_code}", response_model=UserRead, tags=["Register"])
async def validate_user_email(email: EmailStr, validation_code: str):
    validation = get_email_validation(email)
    if not validation:
        raise HTTPException(
            status_code=404, detail=f"Email {email} is not registered")
    if check_validation_code(validation, validation_code) == True:
        user = get_user_by_email(email)
        update_user(user, UserUpdate(username=user.username,
                    email_validation=True, disabled=False))
        return user
    else:
        raise HTTPException(
            status_code=400, detail="Validation code is not valid")
