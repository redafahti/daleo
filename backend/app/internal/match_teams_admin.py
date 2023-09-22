from fastapi import APIRouter, Security, HTTPException, Depends
from ..dependencies import oauth2_scheme, get_current_active_user, get_team, get_match, get_team_match_invitation, add_team_match_invitation, get_team_matches_invitations
from ..models import User, MatchRead, TeamMatchInvitation
from datetime import date, time
from typing import List


################################################ Matches Teams Section  ############################################################################################################
match_teams_router = APIRouter(prefix="/match_teams",
                               tags=["Match Teams"],
                               dependencies=[Depends(oauth2_scheme)],
                               responses={404: {"description": "Match Teams Not found"}},)


# get team matches
@match_teams_router.get("/get_team_matches/{team_name}", response_model=List[MatchRead])
async def get_team_matches(team_name: str, current_user: User = Security(get_current_active_user, scopes=["teams"])):
    team = get_team(team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team with team name: {team_name} not found")
    return get_team_matches(team_name)


# Create team match invitation using team name and match id
@match_teams_router.post("/create_team_match_invitation/{team_name}/{match_id}", response_model=TeamMatchInvitation)
async def new_team_match_invitation(team_name: str, match_id: int, invitation_date: date | None = None, invitation_time: time | None = None, invitation_expiry_date: date | None = None, invitation_expiry_time: time | None = None, current_user: User = Security(get_current_active_user, scopes=["admin", "invitations"])):
    if current_user:
        # check if team exists
        team = get_team(team_name)
        if not team:
            raise HTTPException(
                status_code=404, detail=f"Team with name: {team_name} not found")
        # check if match exists
        match = get_match(match_id)
        if not match:
            raise HTTPException(
                status_code=404, detail=f"Match with ID: {match_id} not found")
        # check if team match invitation exists
        team_match_invitation = get_team_match_invitation(
            team_name=team_name, match_id=match_id)
        if team_match_invitation:
            raise HTTPException(
                status_code=404, detail=f"Team with name: {team_name} has already been invited to match with ID: {match_id}")
        # create team match invitation
        new_team_match_invitation = TeamMatchInvitation(team_id=team.team_id, match_id=match_id, invitation_date=invitation_date,
                                                        invitation_time=invitation_time, invitation_expiry_date=invitation_expiry_date, invitation_expiry_time=invitation_expiry_time)
        # add team match invitation to database
        add_team_match_invitation(new_team_match_invitation)
        return new_team_match_invitation
    else:
        raise HTTPException(
            status_code=404, detail=f"You are not authorized to create team match invitation")


# Read team match invitation
@match_teams_router.get("/get_team_match_invitation", response_model=TeamMatchInvitation)
async def read_team_match_invitation(team_name: str, match_id: int, current_user: User = Security(get_current_active_user, scopes=["admin", "invitations"])):
    if current_user:
        # check if team exists
        team = get_team(team_name=team_name)
        if not team:
            raise HTTPException(
                status_code=404, detail=f"Team with name: {team_name} not found")
        # check if match exists
        match = get_match(match_id=match_id)
        if not match:
            raise HTTPException(
                status_code=404, detail=f"Match with ID: {match_id} not found")
        # check if team match invitation exists
        team_match_invitation = get_team_match_invitation(
            team_name=team_name, match_id=match_id)
        if not team_match_invitation:
            raise HTTPException(
                status_code=404, detail=f"Team with name: {team_name} has NOT been invited to match with ID: {match_id}")
        return team_match_invitation
    else:
        raise HTTPException(
            status_code=404, detail=f"You are not authorized to view team match invitation")


# Read all team match invitations by team name
@match_teams_router.get("/get_team_match_invitations/{team_name}", response_model=List[TeamMatchInvitation])
async def read_team_match_invitations(team_name: str, current_user: User = Security(get_current_active_user, scopes=["admin", "invitations"])):
    if current_user:
        # check if team exists
        team = get_team(team_name)
        if not team:
            raise HTTPException(
                status_code=404, detail=f"Team with name: {team_name} not found")
        # get all team match invitations
        team_match_invitations = get_team_matches_invitations(team_name)
        return team_match_invitations
    else:
        raise HTTPException(
            status_code=404, detail=f"You are not authorized to view team match invitations")
