from sqlmodel import SQLModel, Field, UniqueConstraint, PrimaryKeyConstraint, ForeignKeyConstraint, Relationship
from pydantic import EmailStr
from sqlalchemy.orm import relationship as sa_relationship
from datetime import date, time, datetime
from typing import List


###### Token Section ########################################################################################
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None
    scopes: list[str] = []


###### User Section ###########################################################################################
class UserBase(SQLModel):
    username: str = Field(default=None, index=True)
    hashed_password: str = Field(default=None)
    email: EmailStr = Field(default=None, index=True)
    mobile: str | None = None
    user_photo: str | None = None
    first_name: str | None = None
    last_name:  str | None = None
    gender: str | None = None
    date_of_birth: date | None = None
    mobile_validation: bool | None = False
    email_validation: bool | None = False
    disabled: bool | None = False
    is_admin: bool | None = False
    is_superuser: bool | None = False

    player_id: int | None = None
    coach_id: int | None = None
    referee_id: int | None = None
    manager_id: int | None = None
    FirebaseID: str | None = None
    ExpoPushToken: str | None = None


class User(UserBase, table=True):
    id: int = Field(default=None)

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('username'),
        UniqueConstraint('mobile'),
        UniqueConstraint('email'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['coach_id'], ['coach.coach_id']),
        ForeignKeyConstraint(['referee_id'], ['referee.referee_id']),
        ForeignKeyConstraint(['manager_id'], ['manager.manager_id']),
    )


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    username: str
    password: str | None = None
    email: EmailStr | None = None
    mobile: str | None = None
    user_photo: str | None = None
    first_name: str | None = None
    last_name:  str | None = None
    gender: str | None = None
    date_of_birth: date | None = None
    player_id: int | None = None
    coach_id: int | None = None
    referee_id: int | None = None
    manager_id: int | None = None
    disabled: bool | None = None
    mobile_validation: bool | None = None
    email_validation: bool | None = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
    FirebaseID: str | None = None
    ExpoPushToken: str | None = None


###### Email validation Section ####################################################################################
class EmailValidation(SQLModel, table=True):
    email: EmailStr = Field(default=None, index=True)
    subject: str = Field(default=None)
    email_validation_code: str = Field(default=None)
    email_validation_expiration: datetime = Field(default=None)

    user_id: int = Field(default=None, index=True)

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('email', 'email_validation_code'),
        # Create a composite primary key and a foreign key
        ForeignKeyConstraint(['user_id'], ['user.id']),
    )


###### Manager Section ###############################################################################################
class ManagerBase(SQLModel):
    username: str = Field(default=None, index=True)
    manager_season_rate: int | None = None
    manager_longitude: float | None = None
    manager_latitude: float | None = None
    manager_rating_count: int | None = 0
    manager_rating: float | None = 0.0

    user_id: int = Field(default=None, index=True)


class Manager(ManagerBase, table=True):
    manager_id: int = Field(default=None)

    teams: List["Team"] = Relationship(back_populates="team_manager")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('manager_id'),
        ForeignKeyConstraint(['user_id'], ['user.id']),
    )


class ManagerRead(ManagerBase):
    manager_id: int


class ManagerCreate(ManagerBase):
    user_id: int


class ManagerUpdate(SQLModel):
    username: str = Field(default=None, index=True)
    manager_season_rate: int | None = None
    manager_longitude: float | None = None
    manager_latitude: float | None = None
    manager_rating_count: int | None = 0
    manager_rating: float | None = 0.0


###### Stadium Players Section #################################################################################
class StadiumPlayerLink(SQLModel, table=True):
    player_id: int = Field(default=None)
    stadium_id: int = Field(default=None)
    number_of_matches: int | None = 0
    stadium_rating: int | None = 0

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('player_id', 'stadium_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['stadium_id'], ['stadium.stadium_id']),
    )


###### Match Players Section #################################################################################
class MatchPlayerLink(SQLModel, table=True):
    player_id: int = Field(default=None)
    match_id: int = Field(default=None)
    player_position: str | None = None
    player_rating_count: int | None = 0
    player_rating: float | None = 0.0
    player_goals: int | None = 0
    player_yellow_cards: int | None = 0
    player_red_cards: int | None = 0
    player_penalties_scored: int | None = 0
    player_penalties_missed: int | None = 0

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('player_id', 'match_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['match_id'], ['match.match_id']),
    )


###### Match Player Invitation Section ###############################################################################################
class PlayerMatchInvitationBase(SQLModel):
    message: str | None = None
    invitation_date: date | None = None
    invitation_time: time | None = None
    invitation_expiry_date: date | None = None
    invitation_expiry_time: time | None = None
    is_accepted: bool = Field(default=False)

    player_id: int = Field(default=None, index=True)
    match_id: int = Field(default=None, index=True)


class PlayerMatchInvitation(PlayerMatchInvitationBase, table=True):
    invitation_id: int = Field(default=None)

    player: "Player" = Relationship(back_populates="match_invitations")
    match: "Match" = Relationship(back_populates="player_invitations")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('invitation_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['match_id'], ['match.match_id']),
    )


###### Match Player Request Section ###############################################################################################
class PlayerMatchRequestBase(SQLModel):
    message: str | None = None
    request_date: date | None = None
    request_time: time | None = None
    request_expiry_date: date | None = None
    request_expiry_time: time | None = None
    is_accepted: bool = Field(default=False)

    player_id: int = Field(default=None, index=True)
    match_id: int = Field(default=None, index=True)


class PlayerMatchRequest(PlayerMatchRequestBase, table=True):
    request_id: int = Field(default=None)

    player: "Player" = Relationship(back_populates="match_requests")
    match: "Match" = Relationship(back_populates="player_requests")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('request_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['match_id'], ['match.match_id']),
    )


############################### Team Players Section #################################################################################
class TeamPlayerLink(SQLModel, table=True):
    player_id: int = Field(default=None)
    team_id: int = Field(default=None)
    is_captain: bool = Field(default=False)

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('player_id', 'team_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
    )


################################# Team Player Invitations Section ###############################################################################################
class PlayerTeamInvitationBase(SQLModel):
    message: str | None = None
    invitation_date: date | None = None
    invitation_time: time | None = None
    invitation_expiry_date: date | None = None
    invitation_expiry_time: time | None = None
    is_accepted: bool = Field(default=False)

    player_id: int = Field(default=None, index=True)
    team_id: int = Field(default=None, index=True)


class PlayerTeamInvitation(PlayerTeamInvitationBase, table=True):
    invitation_id: int = Field(default=None)

    player: "Player" = Relationship(back_populates="team_invitations")
    team: "Team" = Relationship(back_populates="player_invitations")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('invitation_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
    )


##################################### Team Player Requests Section ###############################################################################################
class PlayerTeamRequestBase(SQLModel):
    message: str | None = None
    request_date: date | None = None
    request_time: time | None = None
    request_expiry_date: date | None = None
    request_expiry_time: time | None = None
    is_accepted: bool = Field(default=False)

    player_id: int = Field(default=None, index=True)
    team_id: int = Field(default=None, index=True)


class PlayerTeamRequest(PlayerTeamRequestBase, table=True):
    request_id: int = Field(default=None)

    player: "Player" = Relationship(back_populates="team_requests")
    team: "Team" = Relationship(back_populates="player_requests")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('request_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
    )


##################################### Coach Player Requests Section ###############################################################################################
class PlayerCoachRequestBase(SQLModel):
    message: str | None = None
    request_date: date | None = None
    request_time: time | None = None
    request_expiry_date: date | None = None
    request_expiry_time: time | None = None
    is_accepted: bool = Field(default=False)

    player_id: int = Field(default=None, index=True)
    coach_id: int = Field(default=None, index=True)


class PlayerCoachRequest(PlayerCoachRequestBase, table=True):
    request_id: int = Field(default=None)

    player: "Player" = Relationship(back_populates="coach_requests")
    coach: "Coach" = Relationship(back_populates="player_requests")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('request_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['coach_id'], ['coach.coach_id']),
    )


##################################### Player Availability Section #####################################################################################
class PlayerAvailabilityBase(SQLModel):
    available_from: datetime | None = None
    available_to: datetime | None = None

    player_id: int = Field(default=None, index=True)


class PlayerAvailability(PlayerAvailabilityBase, table=True):
    availability_id: int = Field(default=None)

    player: "Player" = Relationship(back_populates="availabilities")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('availability_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
    )


###################################### Players Section ###############################################################################################
class PlayerBase(SQLModel):
    username: str = Field(default=None, index=True)
    player_longitude: float | None = None
    player_latitude: float | None = None
    player_height: float | None = None
    player_weight: float | None = None
    player_foot: str | None = None
    favorite_position: str | None = None
    join_team: bool = Field(default=True)
    join_match: bool = Field(default=True)
    total_rating_count: int | None = 0
    total_rating: float | None = 0.0
    total_matches_played: int | None = 0
    total_matches_won: int | None = 0
    total_matches_lost: int | None = 0
    total_matches_drawn: int | None = 0
    total_goals: int | None = 0
    total_assists: int | None = 0
    total_yellow_cards: int | None = 0
    total_red_cards: int | None = 0
    total_penalties_scored: int | None = 0
    total_penalties_missed: int | None = 0

    user_id: int = Field(default=None, index=True)
    coach_id: int | None = Field(default=None, index=True)


class Player(PlayerBase, table=True):
    player_id: int = Field(default=None)

    availabilities: List["PlayerAvailability"] = Relationship(
        back_populates="player")
    player_coach: "Coach" = Relationship(back_populates="players")
    teams: List["Team"] = Relationship(
        back_populates="players", link_model=TeamPlayerLink)
    captain_of_teams: List["Team"] = Relationship(
        back_populates="team_captain")
    team_invitations: List["PlayerTeamInvitation"] = Relationship(
        back_populates="player")
    team_requests: List["PlayerTeamRequest"] = Relationship(
        back_populates="player")
    match_invitations: List["PlayerMatchInvitation"] = Relationship(
        back_populates="player")
    match_requests: List["PlayerMatchRequest"] = Relationship(
        back_populates="player")
    matches: List["Match"] = Relationship(
        back_populates="players", link_model=MatchPlayerLink)
    stadiums: List["Stadium"] = Relationship(
        back_populates="players", link_model=StadiumPlayerLink)
    coach_requests: List["PlayerCoachRequest"] = Relationship(
        back_populates="player")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('player_id'),
        ForeignKeyConstraint(['user_id'], ['user.id']),
        ForeignKeyConstraint(['coach_id'], ['coach.coach_id']),
    )


class PlayerRead(PlayerBase):
    player_id: int


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(SQLModel):
    username: str | None = None
    player_longitude: float | None = None
    player_latitude: float | None = None
    player_height: int | None = None
    player_weight: int | None = None
    player_foot: str | None = None
    favorite_position: str | None = None
    total_rating_count: int | None = 0
    total_rating: float | None = 0.0
    total_matches_played: int | None = 0
    total_matches_won: int | None = 0
    total_matches_lost: int | None = 0
    total_matches_drawn: int | None = 0
    total_goals: int | None = 0
    total_assists: int | None = 0
    total_yellow_cards: int | None = 0
    total_red_cards: int | None = 0
    total_penalties_scored: int | None = 0
    total_penalties_missed: int | None = 0
    coach_id: int | None = Field(default=None, index=True)


###################################### Stadium Teams Section #################################################################################
class StadiumTeamLink(SQLModel, table=True):
    team_id: int = Field(default=None)
    stadium_id: int = Field(default=None)
    home_team: bool = Field(default=False)

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('team_id', 'stadium_id'),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
        ForeignKeyConstraint(['stadium_id'], ['stadium.stadium_id']),
    )


####################################### Team Matches Section #################################################################################
class MatchTeamLink(SQLModel, table=True):
    match_id: int = Field(default=None)
    team_id: int = Field(default=None)
    is_home_team: bool = Field(default=False)
    team_rating_count: int | None = 0
    team_rating: float | None = 0.0
    team_goals_scored: int | None = 0
    team_goals_conceded: int | None = 0
    team_yellow_cards: int | None = 0
    team_red_cards: int | None = 0
    team_penalties_scored: int | None = 0
    team_penalties_missed: int | None = 0
    match_result: str | None = 'D'
    match_points: int | None = 1

    manager_id: int = Field(default=None, index=True)

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('match_id'),
        ForeignKeyConstraint(['match_id'], ['match.match_id']),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
        ForeignKeyConstraint(['manager_id'], ['manager.manager_id']),
    )


##################################### Match Team Invitation Section ###############################################################################################
class TeamMatchInvitationBase(SQLModel):
    message: str | None = None
    invitation_date: date | None = None
    invitation_time: time | None = None
    invitation_expiry_date: date | None = None
    invitation_expiry_time: time | None = None
    is_accepted: bool = Field(default=False)

    team_id: int = Field(default=None, index=True)
    match_id: int = Field(default=None, index=True)


class TeamMatchInvitation(TeamMatchInvitationBase, table=True):
    invitation_id: int = Field(default=None)

    team: "Team" = Relationship(back_populates="match_invitations")
    match: "Match" = Relationship(back_populates="team_invitations")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('invitation_id'),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
        ForeignKeyConstraint(['match_id'], ['match.match_id']),
    )


#################################### Match Team Request Section ###############################################################################################
class TeamMatchRequestBase(SQLModel):
    message: str | None = None
    request_date: date | None = None
    request_time: time | None = None
    request_expiry_date: date | None = None
    request_expiry_time: time | None = None
    is_accepted: bool = Field(default=False)

    team_id: int = Field(default=None, index=True)
    match_id: int = Field(default=None, index=True)


class TeamMatchRequest(TeamMatchRequestBase, table=True):
    request_id: int = Field(default=None)

    team: "Team" = Relationship(back_populates="match_requests")
    match: "Match" = Relationship(back_populates="team_requests")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('request_id'),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
        ForeignKeyConstraint(['match_id'], ['match.match_id']),
    )


##################################### Coach Team Requests Section ###############################################################################################
class TeamCoachRequestBase(SQLModel):
    message: str | None = None
    request_date: date | None = None
    request_time: time | None = None
    request_expiry_date: date | None = None
    request_expiry_time: time | None = None
    is_accepted: bool = Field(default=False)

    team_id: int = Field(default=None, index=True)
    coach_id: int = Field(default=None, index=True)


class TeamCoachRequest(TeamCoachRequestBase, table=True):
    request_id: int = Field(default=None)

    team: "Team" = Relationship(back_populates="coach_requests")
    coach: "Coach" = Relationship(back_populates="team_requests")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('request_id'),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
        ForeignKeyConstraint(['coach_id'], ['coach.coach_id']),
    )


##################################### Team Availability Section #####################################################################################
class TeamAvailabilityBase(SQLModel):
    available_from: datetime | None = None
    available_to: datetime | None = None
    available_players_count: int | None = None

    team_id: int = Field(default=None, index=True)


class TeamAvailability(TeamAvailabilityBase, table=True):
    availability_id: int = Field(default=None)

    team: "Team" = Relationship(back_populates="availabilities")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('availability_id'),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
    )


############################################### Team Bookings #############################################################################################
class TeamBooking(SQLModel, table=True):
    team_id: int = Field(default=None, index=True)
    booking_id: int = Field(default=None, index=True)

    # create composite primary key and foreign key
    __table_args__ = (
        PrimaryKeyConstraint('team_id', 'booking_id'),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
        ForeignKeyConstraint(['booking_id'], ['booking.booking_id']),
    )


############################################### Team Section ###############################################################################################
class TeamBase(SQLModel):
    team_name: str = Field(default=None, index=True)
    team_logo: str | None = None
    team_home_color_jersey: str | None = None
    team_away_color_jersey: str | None = None
    team_home_color_shorts: str | None = None
    team_away_color_shorts: str | None = None
    total_rating_count: int | None = 0
    total_rating: float | None = 0.0
    total_matches: int | None = 0
    total_matches_won: int | None = 0
    total_matches_lost: int | None = 0
    total_matches_drawn: int | None = 0
    total_goals_scored: int | None = 0
    total_goals_conceded: int | None = 0
    total_yellow_cards: int | None = 0
    total_red_cards: int | None = 0
    total_penalties_scored: int | None = 0
    total_penalties_missed: int | None = 0

    manager_id: int = Field(default=None, index=True)
    coach_id: int = Field(default=None, index=True)
    captain_id: int = Field(default=None, index=True)
    home_stadium_id: int = Field(default=None, index=True)


class Team(TeamBase, table=True):
    team_id: int = Field(default=None)

    players: List["Player"] = Relationship(
        back_populates="teams", link_model=TeamPlayerLink)
    team_manager: "Manager" = Relationship(back_populates="teams")
    team_coach: "Coach" = Relationship(back_populates="teams")
    team_captain: "Player" = Relationship(back_populates="captain_of_teams")
    home_stadium: "Stadium" = Relationship(back_populates="home_teams")
    matches: List["Match"] = Relationship(
        back_populates="teams", link_model=MatchTeamLink)
    availabilities: List["TeamAvailability"] = Relationship(
        back_populates="team")
    match_invitations: List["TeamMatchInvitation"] = Relationship(
        back_populates="team")
    match_requests: List["TeamMatchRequest"] = Relationship(
        back_populates="team")
    player_invitations: List["PlayerTeamInvitation"] = Relationship(
        back_populates="team")
    player_requests: List["PlayerTeamRequest"] = Relationship(
        back_populates="team")
    coach_requests: List["TeamCoachRequest"] = Relationship(
        back_populates="team")
    bookings: List["Booking"] = Relationship(back_populates="teams", link_model=TeamBooking)

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('team_id'),
        UniqueConstraint('team_name'),
        ForeignKeyConstraint(['manager_id'], ['manager.manager_id']),
        ForeignKeyConstraint(['coach_id'], ['coach.coach_id']),
        ForeignKeyConstraint(['home_stadium_id'], ['stadium.stadium_id']),
        ForeignKeyConstraint(['captain_id'], ['player.player_id']),
    )


class TeamRead(TeamBase):
    team_id: int


class TeamCreate(TeamBase):
    pass


class TeamUpdate(SQLModel):
    team_name: str = Field(default=None, index=True)
    team_logo: str | None = None
    team_home_color_jersey: str | None = None
    team_away_color_jersey: str | None = None
    team_home_color_shorts: str | None = None
    team_away_color_shorts: str | None = None
    total_rating_count: int | None = 0
    total_rating: float | None = 0.0
    total_matches: int | None = 0
    total_matches_won: int | None = 0
    total_matches_lost: int | None = 0
    total_matches_drawn: int | None = 0
    total_goals: int | None = 0
    total_yellow_cards: int | None = 0
    total_red_cards: int | None = 0
    total_penalties_scored: int | None = 0
    total_penalties_missed: int | None = 0


######################################### Stadium Coaches Section ##################################################################################################
class StadiumCoachLink(SQLModel, table=True):
    coach_id: int = Field(default=None)
    stadium_id: int = Field(default=None)
    is_home_stadium: bool = Field(default=False)

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('coach_id', 'stadium_id'),
        ForeignKeyConstraint(['coach_id'], ['coach.coach_id']),
        ForeignKeyConstraint(['stadium_id'], ['stadium.stadium_id']),
    )


###### Stadium Referees Section #################################################################################
class StadiumRefereeLink(SQLModel, table=True):
    referee_id: int = Field(default=None)
    stadium_id: int = Field(default=None)
    number_of_matches: int | None = 0
    stadium_rating: int | None = 0

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('referee_id', 'stadium_id'),
        ForeignKeyConstraint(['referee_id'], ['referee.referee_id']),
        ForeignKeyConstraint(['stadium_id'], ['stadium.stadium_id']),
    )


####################################### Match Coaches Section #####################################################################################################
class MatchCoachLink(SQLModel, table=True):
    match_id: int = Field(default=None)
    coach_id: int = Field(default=None)
    match_won: bool | None = None
    match_lost: bool | None = None
    match_draw: bool | None = None

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('match_id', 'coach_id'),
        ForeignKeyConstraint(['match_id'], ['match.match_id']),
        ForeignKeyConstraint(['coach_id'], ['coach.coach_id']),
    )


######################################### Team Coaches Section #####################################################################################################
class TeamCoachLink(SQLModel, table=True):
    team_id: int = Field(default=None)
    coach_id: int = Field(default=None)
    team_coach_rating_count: int | None = 0
    team_coach_rating: float | None = 0.0
    total_matches: int | None = 0
    total_matches_won: int | None = 0
    total_marches_lost: int | None = 0
    total_matches_drawn: int | None = 0

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('team_id', 'coach_id'),
        ForeignKeyConstraint(['team_id'], ['team.team_id']),
        ForeignKeyConstraint(['coach_id'], ['coach.coach_id']),
    )


####################################### Player Coaches Section #####################################################################################################
class PlayerCoachLink(SQLModel, table=True):
    player_id: int = Field(default=None)
    coach_id: int = Field(default=None)
    player_coach_rating_count: int | None = 0
    player_coach_rating: float | None = 0.0

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('player_id', 'coach_id'),
        ForeignKeyConstraint(['player_id'], ['player.player_id']),
        ForeignKeyConstraint(['coach_id'], ['coach.coach_id']),
    )


############################## Coach Section ###############################################################################################
class CoachBase(SQLModel):
    username: str = Field(default=None, index=True)
    coach_player_hourly_rate: int | None = None
    coach_team_hourly_rate: int | None = None
    coach_longitude: float | None = None
    coach_latitude: float | None = None
    total_rating_count: int | None = 0
    total_rating: float | None = 0.0
    total_matches: int | None = 0
    total_matches_won: int | None = 0
    total_matches_lost: int | None = 0
    total_draw_matches: int | None = 0

    user_id: int = Field(default=None, index=True)


class Coach(CoachBase, table=True):
    coach_id: int = Field(default=None)

    players: List["Player"] = Relationship(back_populates="player_coach")
    teams: List["Team"] = Relationship(back_populates="team_coach")

    stadiums: List["Stadium"] = Relationship(
        back_populates="coaches",
        link_model=StadiumCoachLink,
        sa_relationship=sa_relationship("Stadium",
                                        secondary="stadiumcoachlink",
                                        primaryjoin="coach.coach_id==stadiumcoachlink.coach_id",
                                        secondaryjoin="stadium.stadium_id==stadiumcoachlink.stadium_id"
                                        )
    )

    matches: List["Match"] = Relationship(
        back_populates="coaches", link_model=MatchCoachLink)
    player_requests: List["PlayerCoachRequest"] = Relationship(
        back_populates="coach")
    team_requests: List["TeamCoachRequest"] = Relationship(
        back_populates="coach")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('coach_id'),
        ForeignKeyConstraint(['user_id'], ['user.id']),
    )


class CoachRead(CoachBase):
    coach_id: int


class CoachCreate(CoachBase):
    pass


class CoachUpdate(SQLModel):
    username: str = Field(default=None, index=True)
    coach_hourly_rate: int | None = None
    total_rating_count: int | None = 0
    total_rating: float | None = 0.0
    total_matches: int | None = 0
    total_won_matches: int | None = 0
    total_lost_matches: int | None = 0
    total_draw_matches: int | None = 0


###################################### Stadium Section ##############################################################################################
class StadiumBase(SQLModel):
    stadium_name: str = Field(default=None, index=True)
    number_of_pitches: int | None = 1
    stadium_image_url: str | None = Field(default=None, index=True)
    stadium_contact_name: str | None = Field(default=None, index=True)
    stadium_email: EmailStr | None = None
    stadium_website: str | None = None
    stadium_phone_number: str | None = None
    stadium_address: str | None = None
    stadium_longitude: float | None = None
    stadium_latitude: float | None = None
    stadium_neighborhood: str | None = None
    stadium_city: str | None = Field(default=None, index=True)
    stadium_opening_time: datetime | None = Field(default=None, index=True)
    stadium_closing_time: datetime | None = Field(default=None, index=True)
    stadium_open_now: bool | None = Field(default=None, index=True)
    stadium_rating_total: int | None = 0
    stadium_rating: float | None = 0.0

    google_place_id: str = Field(default=None, index=True)
    google_image_reference: str | None = None
    stadium_manager_id: int = Field(default=None, index=True)


class Stadium(StadiumBase, table=True):
    stadium_id: int = Field(default=None, index=True)

    players: List["Player"] = Relationship(
        back_populates="stadiums", link_model=StadiumPlayerLink)
    coaches: List["Coach"] = Relationship(
        back_populates="stadiums",
        link_model=StadiumCoachLink,
        sa_relationship=sa_relationship(
            "Coach",
            secondary="stadiumcoachlink",
            primaryjoin="coach.coach_id==stadiumcoachlink.coach_id",
            secondaryjoin="stadium.stadium_id==stadiumcoachlink.stadium_id"
        )
    )
    home_teams: List["Team"] = Relationship(
        back_populates="home_stadium")
    matches: List["Match"] = Relationship(back_populates="stadium")
    bookings: List["Booking"] = Relationship(back_populates="stadium")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('stadium_id'),
        ForeignKeyConstraint(['stadium_manager_id'], ['user.id']),
        UniqueConstraint('stadium_longitude', 'stadium_latitude'),
    )
    


class StadiumRead(StadiumBase):
    stadium_id: int


class StadiumCreate(StadiumBase):
    pass


class StadiumUpdate(SQLModel):
    stadium_name: str | None = None
    number_of_pitches: int | None = None
    stadium_image_url: str | None = None
    stadium_contact_name: str | None = None
    stadium_email: EmailStr | None = None
    stadium_phone_number: str | None = None
    stadium_website: str | None = None
    stadium_address: str | None = None
    stadium_longitude: float | None = None
    stadium_latitude: float | None = None
    stadium_neighborhood: str | None = None
    stadium_city: str | None = None
    stadium_opening_time: datetime | None = None
    stadium_closing_time: datetime | None = None
    stadium_open_now: bool | None = None
    stadium_rating_total: int | None = None
    stadium_rating: float | None = None
    google_place_id: str | None = None
    google_image_reference: str | None = None
    stadium_manager_id: int | None = None


################################## Match Section #################################################################################################################
class MatchBase(SQLModel):
    home_team_name: str = Field(default=None, index=True)
    away_team_name: str = Field(default=None, index=True)
    match_duration: int = Field(default=None, index=True)
    match_start_time: datetime = Field(default=None, index=True)
    stadium_name: str = Field(default=None, index=True)
    teams_size: int = Field(default=None, index=True)
    number_of_substitutes: int = Field(default=None, index=True)
    match_type: str | None = None
    match_prize: int | None = None

    stadium_id: int = Field(default=None)
    home_team_id: int = Field(default=None)
    away_team_id: int = Field(default=None)
    referee_id: int | None = None


class Match(MatchBase, table=True):
    match_id: int = Field(default=None)

    referee: "Referee" = Relationship(back_populates="matches")
    players: List["Player"] = Relationship(
        back_populates="matches", link_model=MatchPlayerLink)
    coaches: List["Coach"] = Relationship(
        back_populates="matches", link_model=MatchCoachLink)
    stadium: "Stadium" = Relationship(back_populates="matches")
    teams: List["Team"] = Relationship(
        back_populates="matches", link_model=MatchTeamLink)

    team_invitations: List["TeamMatchInvitation"] = Relationship(
        back_populates="match")
    team_requests: List["TeamMatchRequest"] = Relationship(
        back_populates="match")
    player_invitations: List["PlayerMatchInvitation"] = Relationship(
        back_populates="match")
    player_requests: List["PlayerMatchRequest"] = Relationship(
        back_populates="match")

   # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('match_id'),
        ForeignKeyConstraint(['stadium_id'], ['stadium.stadium_id']),
        ForeignKeyConstraint(['home_team_id'], ['team.team_id']),
        ForeignKeyConstraint(['away_team_id'], ['team.team_id']),
        ForeignKeyConstraint(['referee_id'], ['referee.referee_id']),
    )


class MatchRead(MatchBase):
    match_id: int


class MatchCreate(MatchBase):
    pass


class MatchUpdate(SQLModel):
    home_team_name: str = Field(default=None, index=True)
    away_team_name: str = Field(default=None, index=True)
    match_duration: int = Field(default=None, index=True)
    match_start_time: datetime = Field(default=None, index=True)
    stadium_name: str = Field(default=None, index=True)
    teams_size: int = Field(default=None, index=True)
    number_of_substitutes: int = Field(default=None, index=True)
    match_type: str | None = None
    match_prize: int | None = None

################################### Match Score Section ##########################################################################################


class MatchScoreBase(SQLModel):
    home_team_name: str = Field(default=None, index=True)
    away_team_name: str = Field(default=None, index=True)
    home_team_goals_scored: int | None = 0
    away_team_goals_scored: int | None = 0
    home_team_goals_conceded: int | None = 0
    away_team_goals_conceded: int | None = 0
    home_team_yellow_cards: int | None = 0
    away_team_yellow_cards: int | None = 0
    home_team_red_cards: int | None = 0
    away_team_red_cards: int | None = 0
    home_team_penalties_scored: int | None = 0
    away_team_penalties_scored: int | None = 0
    home_team_penalties_missed: int | None = 0
    away_team_penalties_missed: int | None = 0

    winner_team: str = Field(default=None, index=True)
    loser_team: str = Field(default=None, index=True)
    draw_match: bool = Field(default=True, index=True)

    home_team_id: int = Field(default=None)
    away_team_id: int = Field(default=None)


class MatchScore(MatchScoreBase, table=True):
    match_id: int = Field(default=None)

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('match_id'),
        ForeignKeyConstraint(['match_id'], ['match.match_id']),
        ForeignKeyConstraint(['home_team_id'], ['team.team_id']),
        ForeignKeyConstraint(['away_team_id'], ['team.team_id']),
    )


################################### Referee Section ###############################################################################################
class RefereeBase(SQLModel):
    username: str = Field(default=None, index=True)
    referee_hourly_rate: int | None = None
    referee_longitude: float | None = None
    referee_latitude: float | None = None
    total_rating_count: int | None = 0
    total_rating: float | None = 0.0

    user_id: int = Field(default=None, index=True)


class Referee(RefereeBase, table=True):
    referee_id: int = Field(default=None)

    matches: List["Match"] = Relationship(
        back_populates="referee")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('referee_id'),
        ForeignKeyConstraint(['user_id'], ['user.id']),
    )


class RefereeRead(RefereeBase):
    referee_id: int


class RefereeCreate(RefereeBase):
    pass


class RefereeUpdate(SQLModel):
    username: str = Field(default=None, index=True)
    referee_hourly_rate: int | None = None
    referee_rating_count: int | None = 0
    referee_rating: float | None = 0.0


################## Booking Section ##################################################################################################################
class BookingBase(SQLModel):
    booking_start_time: datetime = Field(default=None, index=True)
    booking_end_time: datetime = Field(default=None, index=True)
    booking_status: str = Field(default=None, index=True)
    booking_price: int | None = None
    booking_type: str = Field(default=None, index=True)
    booking_confirmation_code: str = Field(default=None, index=True)

    stadium_manager_id: int = Field(default=None, index=True)
    match_id: int = Field(default=None, index=True)
    stadium_id: int = Field(default=None, index=True)
    team_manager_id: int = Field(default=None, index=True)


class Booking(BookingBase, table=True):
    booking_id: int = Field(default=None)

    teams: List["Team"] = Relationship(back_populates="bookings", link_model=TeamBooking)
    stadium : "Stadium" = Relationship(back_populates="bookings")

    # Create a composite primary key and a foreign key
    __table_args__ = (
        PrimaryKeyConstraint('booking_id'),
        ForeignKeyConstraint(['match_id'], ['match.match_id']),
        ForeignKeyConstraint(['stadium_id'], ['stadium.stadium_id']),
        ForeignKeyConstraint(['team_manager_id'], ['manager.manager_id']),
    )
    
    