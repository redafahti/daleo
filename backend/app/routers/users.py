from fastapi import Depends, Security, APIRouter, File, UploadFile, Response
from fastapi.responses import FileResponse
from ..models import UserRead, User, UserUpdate
from ..dependencies import oauth2_scheme, get_password_hash, get_current_active_user, get_user, update_user, delete_user, get_email_validation, create_email_validation, send_validation_email, update_email_validation, delete_email_validation, get_manager, get_player, get_coach, get_referee, delete_manager, delete_player, delete_coach, delete_referee
from dotenv import load_dotenv
import os
load_dotenv()

############################# User Section ############################################################################################################
users_router = APIRouter(prefix="/users",
                         tags=["Users"],
                         dependencies=[Depends(oauth2_scheme)],
                         responses={404: {"description": "User not found"}},)


# users root
@users_router.get("/")
async def read_root(current_user: User = Security(get_current_active_user, scopes=["users"])):
    return{"Welcome to Team up Users Section"}


# get my user profile
@users_router.get("/get_user/me", response_model=UserRead)
async def get_my_user_profile(current_user: User = Security(get_current_active_user, scopes=["users"])):
    return current_user


# update my user profile
@users_router.put("/user_update/me", response_model=UserRead)
async def update_my_user_pofile(update: UserUpdate, current_user: User = Security(get_current_active_user, scopes=["users"])):
    user = get_user(username=current_user.username)
    if update.password:
        hashed_password = get_password_hash(update.password)
    hashed_password = user.hashed_password
    if update.email:
        existing_validation = get_email_validation(update.email)
        if not existing_validation:
            new_validation = create_email_validation(user)
        new_validation = update_email_validation(existing_validation)
        send_validation_email(new_validation)
    user_update = User(username=current_user.username, hashed_password=hashed_password, email=update.email, mobile=update.mobile, user_photo=update.user_photo,
                       first_name=update.first_name, last_name=update.last_name, gender=update.gender, date_of_birth=update.date_of_birth)
    return update_user(user, user_update)


@users_router.post("/upload_photo/me", response_model=dict)
def upload_my_photo(file: UploadFile = File(...), current_user: User = Security(get_current_active_user, scopes=["users"])):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_folder = os.path.join(project_root, "public")
    folder_name = f"user_id_{current_user.id}"
    folder_path = os.path.join(public_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    file_name = f"profile_photo_{current_user.id}.jpg"
    file_path = os.path.join(folder_path, file_name)

    try:
        with open(file_path, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    url = f"/public/{folder_name}/{file_name}"  # Construct the relative URL
    return {"url": url}


# download my user photo
@users_router.get("/download_photo/me", response_model=dict)
def download_my_photo(current_user: User = Security(get_current_active_user, scopes=["users"])):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_folder = os.path.join(project_root, "public")
    folder_name = f"user_id_{current_user.id}"
    folder_path = os.path.join(public_folder, folder_name)
    file_name = f"profile_photo_{current_user.id}.jpg"
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name, media_type="image/jpeg")
    else:
        return {"message": "No profile photo found for this user"}


# get my user photo
@users_router.get("/get_photo/me", response_model=dict)
def get_my_photo(current_user: User = Security(get_current_active_user, scopes=["users"])):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_folder = os.path.join(project_root, "public")
    folder_name = f"user_id_{current_user.id}"
    folder_path = os.path.join(public_folder, folder_name)
    file_name = f"profile_photo_{current_user.id}.jpg"
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            photo_data = f.read()
        return Response(content=photo_data, media_type="image/jpeg")
    else:
        return {"message": "No profile photo found for this user"}


# is current user a player
@users_router.get("/user_is_player/me")
async def is_user_player(current_user: User = Security(get_current_active_user, scopes=["users"])):
    # check if current user is a player
    if current_user.player_id is None:
        return False
    return True


# is current user a manager
@users_router.get("/user_is_manager/me")
async def is_user_manager(current_user: User = Security(get_current_active_user, scopes=["users"])):
    # check if current user is a manager
    if current_user.manager_id is None:
        return False
    return True


# is current user a coach
@users_router.get("/user_is_coach/me")
async def is_user_coach(current_user: User = Security(get_current_active_user, scopes=["users"])):
    # check if current user is a coach
    if current_user.coach_id is None:
        return False
    return True


# is current user a referee
@users_router.get("/user_is_referee/me")
async def is_user_referee(current_user: User = Security(get_current_active_user, scopes=["users"])):
    # check if current user is a referee
    if current_user.referee_id is None:
        return False
    return True


# delete current user
@users_router.delete("/user_delete/me")
async def delete_my_user_profile(current_user: User = Security(get_current_active_user, scopes=["users"])):
    # check if current user has a an email validation and delete it if there is
    email_validation = get_email_validation(username=current_user.username)
    if email_validation:
        delete_email_validation(email_validation)
    # check if current user is a manager and delete it if there is
    manager = get_manager(username=current_user.username)
    if manager:
        delete_manager(manager)
    # check if current user is a player and delete it if there is
    player = get_player(username=current_user.username)
    if player:
        delete_player(player)
    # check if current user is a coach and delete it if there is
    coach = get_coach(username=current_user.username)
    if coach:
        delete_coach(coach)
    # check if current user is a referee and delete it if there is
    referee = get_referee(username=current_user.username)
    if referee:
        delete_referee(referee)
    return delete_user(username=current_user.username)
