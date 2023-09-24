/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CoachRead } from '../models/CoachRead';
import type { ManagerRead } from '../models/ManagerRead';
import type { MatchTeamLink } from '../models/MatchTeamLink';
import type { PlayerTeamInvitation } from '../models/PlayerTeamInvitation';
import type { PlayerTeamRequest } from '../models/PlayerTeamRequest';
import type { TeamCoachRequest } from '../models/TeamCoachRequest';
import type { TeamMatchInvitation } from '../models/TeamMatchInvitation';
import type { TeamMatchRequest } from '../models/TeamMatchRequest';
import type { TeamPlayerLink } from '../models/TeamPlayerLink';
import type { TeamRead } from '../models/TeamRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ManagersService {

    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static managersReadRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/',
            errors: {
                404: `Managers Not found`,
            },
        });
    }

    /**
     * Create My Manager Profile
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static managersCreateMyManagerProfile(): CancelablePromise<ManagerRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/managers/create_manager_profile/me',
            errors: {
                404: `Managers Not found`,
            },
        });
    }

    /**
     * Get My Manager Profile
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static managersGetMyManagerProfile(): CancelablePromise<ManagerRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/get_manager_profile/me',
            errors: {
                404: `Managers Not found`,
            },
        });
    }

    /**
     * Update My Manager Profile
     * @param seasonRate
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static managersUpdateMyManagerProfile(
        seasonRate?: number,
    ): CancelablePromise<ManagerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/update_manager_profile/me',
            query: {
                'season_rate': seasonRate,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete My Manager Profile
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static managersDeleteMyManagerProfile(): CancelablePromise<ManagerRead> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/managers/delete_manager_profile/me',
            errors: {
                404: `Managers Not found`,
            },
        });
    }

    /**
     * Create New Team
     * @param teamName
     * @param teamLogo
     * @param teamHomeColorJersey
     * @param teamAwayColorJersey
     * @param teamHomeColorShorts
     * @param teamAwayColorShorts
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static managersCreateNewTeam(
        teamName: string,
        teamLogo?: string,
        teamHomeColorJersey?: string,
        teamAwayColorJersey?: string,
        teamHomeColorShorts?: string,
        teamAwayColorShorts?: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/managers/create_team/{team_name}',
            path: {
                'team_name': teamName,
            },
            query: {
                'team_logo': teamLogo,
                'team_home_color_jersey': teamHomeColorJersey,
                'team_away_color_jersey': teamAwayColorJersey,
                'team_home_color_shorts': teamHomeColorShorts,
                'team_away_color_shorts': teamAwayColorShorts,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Teams
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static managersGetMyTeams(): CancelablePromise<Array<TeamRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/manager_teams/me',
            errors: {
                404: `Managers Not found`,
            },
        });
    }

    /**
     * Update My Team
     * @param teamName
     * @param teamLogo
     * @param teamHomeColorJersey
     * @param teamAwayColorJersey
     * @param teamHomeColorShorts
     * @param teamAwayColorShorts
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static managersUpdateMyTeam(
        teamName: string,
        teamLogo?: string,
        teamHomeColorJersey?: string,
        teamAwayColorJersey?: string,
        teamHomeColorShorts?: string,
        teamAwayColorShorts?: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/update_team/{team_name}',
            path: {
                'team_name': teamName,
            },
            query: {
                'team_logo': teamLogo,
                'team_home_color_jersey': teamHomeColorJersey,
                'team_away_color_jersey': teamAwayColorJersey,
                'team_home_color_shorts': teamHomeColorShorts,
                'team_away_color_shorts': teamAwayColorShorts,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Assign My Team Manager
     * @param teamName
     * @param managerUsername
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static managersAssignMyTeamManager(
        teamName: string,
        managerUsername: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/assign_team_manager/{team_name}/{manager_username}',
            path: {
                'team_name': teamName,
                'manager_username': managerUsername,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete My Team
     * @param teamName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static managersDeleteMyTeam(
        teamName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/managers/delete_team/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add My Team Coach Request
     * @param coachUsername
     * @param message
     * @param requestDate
     * @param requestTime
     * @param requestExpiryDate
     * @param requestExpiryTime
     * @returns TeamCoachRequest Successful Response
     * @throws ApiError
     */
    public static managersAddMyTeamCoachRequest(
        coachUsername: string,
        message?: string,
        requestDate?: string,
        requestTime?: string,
        requestExpiryDate?: string,
        requestExpiryTime?: string,
    ): CancelablePromise<TeamCoachRequest> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/managers/add_my_team_coach_request/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            query: {
                'message': message,
                'request_date': requestDate,
                'request_time': requestTime,
                'request_expiry_date': requestExpiryDate,
                'request_expiry_time': requestExpiryTime,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove My Team Coach Request
     * @param coachUsername
     * @returns any Successful Response
     * @throws ApiError
     */
    public static managersRemoveMyTeamCoachRequest(
        coachUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/managers/remove_my_team_coach_request/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Assign My Team Coach
     * @param coachUsername
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static managersAssignMyTeamCoach(
        coachUsername: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/managers/assign_my_team_coach/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Team Coach
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static managersGetMyTeamCoach(): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/get_my_team_coach/me',
            errors: {
                404: `Managers Not found`,
            },
        });
    }

    /**
     * Rate My Team Coach
     * @param rating
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static managersRateMyTeamCoach(
        rating: number,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/rate_my_team_coach/{rating}',
            path: {
                'rating': rating,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove My Team Coach
     * @param teamName
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static managersRemoveMyTeamCoach(
        teamName: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/managers/remove_team_coach/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Team Players
     * @param teamName
     * @returns TeamPlayerLink Successful Response
     * @throws ApiError
     */
    public static managersGetMyTeamPlayers(
        teamName: string,
    ): CancelablePromise<Array<TeamPlayerLink>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/get_my_team_players/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Team Player
     * @param username
     * @param teamName
     * @returns TeamPlayerLink Successful Response
     * @throws ApiError
     */
    public static managersGetMyTeamPlayer(
        username: string,
        teamName: string,
    ): CancelablePromise<TeamPlayerLink> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/get_my_team_player/{username}/{team_name}',
            path: {
                'username': username,
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Player Team Invitation
     * @param teamName
     * @param playerUsername
     * @param message
     * @returns PlayerTeamInvitation Successful Response
     * @throws ApiError
     */
    public static managersCreatePlayerTeamInvitation(
        teamName: string,
        playerUsername: string,
        message: string,
    ): CancelablePromise<PlayerTeamInvitation> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/managers/create_player_team_invitation/{team_name}/{player_username}',
            path: {
                'team_name': teamName,
                'player_username': playerUsername,
            },
            query: {
                'message': message,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Invite Players By Location
     * @param teamName
     * @param radius
     * @param message
     * @param invitationExpiryDays
     * @returns PlayerTeamInvitation Successful Response
     * @throws ApiError
     */
    public static managersInvitePlayersByLocation(
        teamName: string,
        radius: number,
        message?: string,
        invitationExpiryDays?: number,
    ): CancelablePromise<Array<PlayerTeamInvitation>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/invite_players_by_location/{team_name}/{radius}',
            path: {
                'team_name': teamName,
                'radius': radius,
            },
            query: {
                'message': message,
                'invitation_expiry_days': invitationExpiryDays,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Invite Players By Position
     * @param teamName
     * @param favoritePosition
     * @param radius
     * @param message
     * @param invitationExpiryDays
     * @returns PlayerTeamInvitation Successful Response
     * @throws ApiError
     */
    public static managersInvitePlayersByPosition(
        teamName: string,
        favoritePosition: string,
        radius: number,
        message?: string,
        invitationExpiryDays?: number,
    ): CancelablePromise<Array<PlayerTeamInvitation>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/invite_players_by_position/{team_name}/{favorite_position}/{radius}',
            path: {
                'team_name': teamName,
                'favorite_position': favoritePosition,
                'radius': radius,
            },
            query: {
                'message': message,
                'invitation_expiry_days': invitationExpiryDays,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Invite Players By Rating
     * @param teamName
     * @param rating
     * @param radius
     * @param message
     * @param invitationExpiryDays
     * @returns PlayerTeamInvitation Successful Response
     * @throws ApiError
     */
    public static managersInvitePlayersByRating(
        teamName: string,
        rating: number,
        radius: number,
        message?: string,
        invitationExpiryDays?: number,
    ): CancelablePromise<Array<PlayerTeamInvitation>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/invite_players_by_rating',
            query: {
                'team_name': teamName,
                'rating': rating,
                'radius': radius,
                'message': message,
                'invitation_expiry_days': invitationExpiryDays,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove My Team Player Invitation
     * @param teamName
     * @param playerUsername
     * @param message
     * @returns PlayerTeamInvitation Successful Response
     * @throws ApiError
     */
    public static managersRemoveMyTeamPlayerInvitation(
        teamName: string,
        playerUsername: string,
        message: string,
    ): CancelablePromise<PlayerTeamInvitation> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/managers/remove_my_team_player_invitation/{team_name}/{player_username}',
            path: {
                'team_name': teamName,
                'player_username': playerUsername,
            },
            query: {
                'message': message,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Team Players Requests
     * @param teamName
     * @returns PlayerTeamRequest Successful Response
     * @throws ApiError
     */
    public static managersGetMyTeamPlayersRequests(
        teamName: string,
    ): CancelablePromise<Array<PlayerTeamRequest>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/get_my_team_players_requests/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Player Request
     * @param playerUsername
     * @param teamName
     * @param isAccepted
     * @returns PlayerTeamRequest Successful Response
     * @throws ApiError
     */
    public static managersUpdatePlayerRequest(
        playerUsername: string,
        teamName: string,
        isAccepted: boolean,
    ): CancelablePromise<PlayerTeamRequest> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/update_player_request/{player_username}/{team_name}/{is_accepted}',
            path: {
                'player_username': playerUsername,
                'team_name': teamName,
                'is_accepted': isAccepted,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add My Team Player
     * @param playerUsername
     * @param teamName
     * @param isCaptain
     * @param playerPosition
     * @returns TeamPlayerLink Successful Response
     * @throws ApiError
     */
    public static managersAddMyTeamPlayer(
        playerUsername: string,
        teamName: string,
        isCaptain: boolean = false,
        playerPosition?: string,
    ): CancelablePromise<TeamPlayerLink> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/managers/add_my_team_player/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            query: {
                'team_name': teamName,
                'is_captain': isCaptain,
                'player_position': playerPosition,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove My Team Player
     * @param playerUsername
     * @param teamName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static managersRemoveMyTeamPlayer(
        playerUsername: string,
        teamName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/remove_my_team_player/{player_username}/{team_name}',
            path: {
                'player_username': playerUsername,
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Team Captain
     * @param teamName
     * @returns TeamPlayerLink Successful Response
     * @throws ApiError
     */
    public static managersGetMyTeamCaptain(
        teamName: string,
    ): CancelablePromise<TeamPlayerLink> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/get_my_team_captain/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add My Team Captain
     * @param username
     * @param teamName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static managersAddMyTeamCaptain(
        username: string,
        teamName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/add_my_team_captain/{username}/{team_name}',
            path: {
                'username': username,
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove My Team Captain
     * @param teamName
     * @returns TeamPlayerLink Successful Response
     * @throws ApiError
     */
    public static managersRemoveMyTeamCaptain(
        teamName: string,
    ): CancelablePromise<TeamPlayerLink> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/remove_my_team_captain/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * New Match
     * @param teamName
     * @param matchDuration
     * @param matchStartTime
     * @param teamsSize
     * @param numberOfSubstitutes
     * @param matchType
     * @param matchPrize
     * @param stadiumId
     * @returns MatchTeamLink Successful Response
     * @throws ApiError
     */
    public static managersNewMatch(
        teamName: string,
        matchDuration: number,
        matchStartTime: string,
        teamsSize: number,
        numberOfSubstitutes: number,
        matchType: string,
        matchPrize: number,
        stadiumId: number,
    ): CancelablePromise<MatchTeamLink> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/managers/create_match/{team_name}/{stadium}/{match_duration}/{match_start_time}/{teams_size}/{number_of_substitutes}/{match_type}/{match_prize}',
            path: {
                'team_name': teamName,
                'match_duration': matchDuration,
                'match_start_time': matchStartTime,
                'teams_size': teamsSize,
                'number_of_substitutes': numberOfSubstitutes,
                'match_type': matchType,
                'match_prize': matchPrize,
            },
            query: {
                'stadium_id': stadiumId,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Team Match Invitation
     * @param matchId
     * @param awayTeamName
     * @param message
     * @returns TeamMatchInvitation Successful Response
     * @throws ApiError
     */
    public static managersCreateTeamMatchInvitation(
        matchId: number,
        awayTeamName: string,
        message: string,
    ): CancelablePromise<TeamMatchInvitation> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/managers/create_team_match_invitation/{match_id}/{away_team_name}',
            path: {
                'match_id': matchId,
                'away_team_name': awayTeamName,
            },
            query: {
                'message': message,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Invite Teams By Stadium
     * @param matchId
     * @param stadiumId
     * @param message
     * @param invitationExpiryDays
     * @returns TeamMatchInvitation Successful Response
     * @throws ApiError
     */
    public static managersInviteTeamsByStadium(
        matchId: number,
        stadiumId: number,
        message?: string,
        invitationExpiryDays?: number,
    ): CancelablePromise<Array<TeamMatchInvitation>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/invite_teams_by_stadium/{match_id}/{stadium_id}',
            path: {
                'match_id': matchId,
                'stadium_id': stadiumId,
            },
            query: {
                'message': message,
                'invitation_expiry_days': invitationExpiryDays,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove My Match Team Invitation
     * @param matchId
     * @param teamName
     * @returns TeamMatchInvitation Successful Response
     * @throws ApiError
     */
    public static managersRemoveMyMatchTeamInvitation(
        matchId: number,
        teamName: string,
    ): CancelablePromise<TeamMatchInvitation> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/managers/remove_my_match_team_invitation/{match_id}/{team_name}',
            path: {
                'match_id': matchId,
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Match Teams Requests
     * @param matchId
     * @returns TeamMatchRequest Successful Response
     * @throws ApiError
     */
    public static managersGetMyMatchTeamsRequests(
        matchId: number,
    ): CancelablePromise<Array<TeamMatchRequest>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers/get_my_match_teams_requests/{match_id}',
            path: {
                'match_id': matchId,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Team Request
     * @param teamName
     * @param matchId
     * @param isAccepted
     * @returns TeamMatchRequest Successful Response
     * @throws ApiError
     */
    public static managersUpdateTeamRequest(
        teamName: string,
        matchId: string,
        isAccepted: boolean,
    ): CancelablePromise<TeamMatchRequest> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/update_team_request/{team_name}/{match_id}/{is_accepted}',
            path: {
                'team_name': teamName,
                'match_id': matchId,
                'is_accepted': isAccepted,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove My Match Team
     * @param teamName
     * @param matchId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static managersRemoveMyMatchTeam(
        teamName: string,
        matchId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/managers/remove_my_match_team/{team_name}/{match_id}',
            path: {
                'team_name': teamName,
                'match_id': matchId,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Away Team
     * @param matchId
     * @param teamName
     * @returns MatchTeamLink Successful Response
     * @throws ApiError
     */
    public static managersAddAwayTeam(
        matchId: number,
        teamName: string,
    ): CancelablePromise<MatchTeamLink> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers/add_away_team/{match_id}/{team_name}',
            path: {
                'match_id': matchId,
                'team_name': teamName,
            },
            errors: {
                404: `Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

}
