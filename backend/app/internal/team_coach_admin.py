from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_admin, get_coach, get_coach_teams, get_coach_by_id, get_team, get_team_manager, get_team_coach, add_team_coach, remove_team_coach, update_coach_rating
from ..models import User, TeamRead, PlayerRead, CoachRead
from typing import List


####################################  Team Coaches Section  ############################################################################################################
team_coach_router = APIRouter(prefix="/team_coach",
                              tags=["Team Coach"],
                              dependencies=[Depends(oauth2_scheme)],
                              responses={404: {"description": "Team Coach Not found"}},)


# get coach's teams
@team_coach_router.get("/get_coach_teams/{coach_username}", response_model=List[TeamRead])
async def read_coach_teams(coach_username: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username {coach_username} not found")
    teams = get_coach_teams(coach)
    if not teams:
        raise HTTPException(
            status_code=404, detail=f"Coach {coach_username} is not assigned to any team")
    return teams


# Assign coach to team
@team_coach_router.put("/assign_team_coach/{coach_username}/{team_name}", response_model=PlayerRead)
async def assign_coach_to_team(coach_username: str, team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if coach exists
    coach = get_coach(coach_username)
    if not coach:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} not found")
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if coach already assigned to the team
    team_coach = get_team_coach(team)
    if team_coach and team_coach.coach_id == coach.coach_id:
        raise HTTPException(
            status_code=404, detail=f"Coach with username: {coach_username} is already assigned to the {team_name} team")
    # assign coach to team
    return add_team_coach(team, coach)


# remove coach from team
@team_coach_router.put("/remove_team_coach/{team_name}", response_model=PlayerRead)
async def remove_coach_from_team(team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if team has a coach
    team_coach = get_team_coach(team)
    if not team_coach:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} has no coach")
    # remove coach from team
    return remove_team_coach(team)


# get Team coach
@team_coach_router.get("/get_team_coach/{team_name}", response_model=CoachRead)
async def read_team_coach(team_name: str, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # check if team has a coach
    team_coach = get_team_coach(team)
    if not team_coach:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} has no coach")
    return team_coach


# rate team's coach
@team_coach_router.put("/rate_player_coach/{username}/{rating}", response_model=CoachRead)
async def rate_my_coach(team_name: str, rating: int, current_admin: User = Security(get_current_active_admin, scopes=["admin"])):
    # check if current team exists
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} not found")
    # get team's coach
    team_coach = get_team_coach(team)
    # check if coach exists
    if not team_coach:
        raise HTTPException(
            status_code=404, detail=f"Team with name {team_name} has no coach")
    # check if current user is the team manager
    team_manager = get_team_manager(team)
    if team_manager.user_id != current_admin.id:
        raise HTTPException(
            status_code=400, detail=f"Current user is not the team manager")
    # Check if the manager_rating is between 0 and 5
    if rating < 0 or rating > 5:
        raise HTTPException(
            status_code=400, detail="Coach rating must be between 0 and 5"
        )
    # get coach by id
    coach = get_coach_by_id(team_coach.coach_id)
    # Update coach
    return update_coach_rating(coach)
