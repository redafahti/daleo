from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_user, update_user, get_current_active_admin, get_users, delete_user, get_password_hash, create_user, create_email_validation, get_email_validation, send_validation_email, delete_email_validation, get_manager, delete_manager, get_player, delete_player, get_coach, delete_coach,  get_referee, delete_referee
from ..models import User, UserUpdate, UserRead
from pydantic import EmailStr
from datetime import date


########################### Users Admin Section ############################################################################################################
users_admin_router = APIRouter(
    prefix="/users_admin",
    tags=["Users Admin"],
    dependencies=[Depends(oauth2_scheme)],
    responses={418: {"description": "I'm a User Administrator"}},)


# get all users
@users_admin_router.get("/all_users", response_model=list[UserRead])
async def get_all_users(current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    return get_users()


# get user profile
@users_admin_router.get("/get_user/{username}", response_model=UserRead)
async def get_user_profile(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    return user


@users_admin_router.post("/new_user", response_model=UserRead)
async def new_user(username: str,
                   password: str,
                   email: EmailStr,
                   mobile: str | None = None,
                   user_photo: str | None = None,
                   first_name: str | None = None,
                   last_name:  str | None = None,
                   gender: str | None = None,
                   date_of_birth: date | None = None,
                   FirebaseID: str | None = None,
                   ExpoPushToken: str | None = None,
                   current_admin: User = Security(
                       get_current_active_admin, scopes=["admin"])
                   ):
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password, email=email,
                    mobile=mobile, first_name=first_name, last_name=last_name, gender=gender, user_photo=user_photo, date_of_birth=date_of_birth, disabled=True, FirebaseID=FirebaseID, ExpoPushToken=ExpoPushToken)
    user = create_user(new_user)
    validation = create_email_validation(user)
    send_validation_email(validation)
    return user


@users_admin_router.put("/user_update", response_model=UserRead)
async def update_user_pofile(update: UserUpdate, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user = get_user(update.username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {update.username} not found")
    if update.password:
        hashed_password = get_password_hash(update.password)
    hashed_password = user.hashed_password
    if update.email:
        validation = get_email_validation(update.email)
        if validation:
            delete_email_validation(validation)
        updated_validation = create_email_validation(user)
        send_validation_email(updated_validation)
    user_update = User(username=update.username,
                       hashed_password=hashed_password,
                       email=update.email,
                       mobile=update.mobile,
                       user_photo=update.user_photo,
                       first_name=update.first_name,
                       last_name=update.last_name,
                       gender=update.gender,
                       date_of_birth=update.date_of_birth,
                       mobile_validation=update.mobile_validation,
                       email_validation=update.email_validation,
                       disabled=update.disabled,
                       player_id=update.player_id,
                       coach_id=update.coach_id,
                       manager_id=update.manager_id,
                       referee_id=update.referee_id,
                       FirebaseID=update.FirebaseID,
                       ExpoPushToken=update.ExpoPushToken)
    return update_user(user, user_update)


# get email validation
@users_admin_router.get("/get_email_validation/{username}", response_model=dict)
async def get_email_validation_by_username(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    validation = get_email_validation(user.email)
    if not validation:
        raise HTTPException(
            status_code=404, detail=f"Email validation for user {username} not found")
    return validation


# Validate email
@users_admin_router.patch("/validate_email/{username}", response_model=dict)
async def validate_user_email(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    update_user(user, UserUpdate(
        email_validation=True, disabled=False))
    return {"message": "email validated successfully"}


# disable user by username
@ users_admin_router.patch("/disable_user/{username}")
async def disable_user_profile(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if user exists
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    # disable user
    update_user(user, UserUpdate(disabled=True))
    return {"message": f"User with username {username} disabled successfully"}


# enable user by username
@users_admin_router.patch("/enable_user/{username}")
async def enable_user_profile(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    update_user(user, UserUpdate(disabled=False))
    return {"message": f"User with username {username} enabled successfully"}


# Validate user mobile by username
@users_admin_router.patch("/validate_mobile/{username}")
async def validate_user_mobile(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    update_user(user, UserUpdate(mobile_validation=True))
    return {"message": f"User with username {username} mobile validated successfully"}


# is user a player
@users_admin_router.get("/user_is_player/{username}")
async def is_user_player(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user_db = get_user(username)
    if not user_db:
        raise HTTPException(
            status_code=404, detail=f"User with {username} not found")
    # check if current user is a player
    if user_db.player_id is None:
        return False
    return True


# is user a manager
@users_admin_router.get("/user_is_manager/{username}")
async def is_user_manager(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user_db = get_user(username)
    if not user_db:
        raise HTTPException(
            status_code=404, detail=f"User with {username} not found")
    # check if current user is a manager
    if user_db.manager_id is None:
        return False
    return True


# is user a coach
@users_admin_router.get("/user_is_coach/{username}")
async def is_user_coach(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user_db = get_user(username)
    if not user_db:
        raise HTTPException(
            status_code=404, detail=f"User with {username} not found")
    # check if current user is a coach
    if user_db.coach_id is None:
        return False
    return True


# is user a referee
@users_admin_router.get("/user_is_referee/{username}")
async def is_user_referee(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user_db = get_user(username)
    if not user_db:
        raise HTTPException(
            status_code=404, detail=f"User with {username} not found")
    # check if current user is a referee
    if user_db.referee_id is None:
        return False
    return True


# delete user
@users_admin_router.delete("/delete_user/{username}")
async def delete_user_profile(username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    # check if user has a email validation and delete it if there is
    validation = get_email_validation(user.email)
    if validation:
        delete_email_validation(validation)
    # check if current user is a manager and delete it if there is
    manager = get_manager(username=username)
    if manager:
        delete_manager(manager)
    # check if current user is a player and delete it if there is
    player = get_player(username=username)
    if player:
        delete_player(player)
    # check if current user is a coach and delete it if there is
    coach = get_coach(username=username)
    if coach:
        delete_coach(coach)
    # check if current user is a referee and delete it if there is
    referee = get_referee(username=username)
    if referee:
        delete_referee(referee)

    return delete_user(username)


# Assign a new Firbase ID to a user
@users_admin_router.patch("/assign_firebase_id/{username}/{FirebaseID}")
async def assign_firebase_id_to_user(username: str, FirebaseID: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with username {username} not found")
    update_user(user, UserUpdate(firebase_id=FirebaseID))
    return {"message": f"User with username {username} assigned a firebase id successfully"}
