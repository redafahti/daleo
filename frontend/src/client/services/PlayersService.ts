/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CoachRead } from '../models/CoachRead';
import type { PlayerAvailability } from '../models/PlayerAvailability';
import type { PlayerCoachRequest } from '../models/PlayerCoachRequest';
import type { PlayerRead } from '../models/PlayerRead';
import type { PlayerTeamInvitation } from '../models/PlayerTeamInvitation';
import type { PlayerTeamRequest } from '../models/PlayerTeamRequest';
import type { TeamPlayerLink } from '../models/TeamPlayerLink';
import type { TeamRead } from '../models/TeamRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PlayersService {

    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersReadRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Create My Player Profile
     * @param playerHeight
     * @param playerWeight
     * @param playerFoot
     * @param favoritePosition
     * @param joinTeam
     * @param joinMatch
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersCreateMyPlayerProfile(
        playerHeight?: number,
        playerWeight?: number,
        playerFoot?: string,
        favoritePosition?: string,
        joinTeam: boolean = true,
        joinMatch: boolean = true,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/players/create_player/me',
            query: {
                'player_height': playerHeight,
                'player_weight': playerWeight,
                'player_foot': playerFoot,
                'favorite_position': favoritePosition,
                'join_team': joinTeam,
                'join_match': joinMatch,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update My Availability
     * @param availableFrom
     * @param availableTo
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersUpdateMyAvailability(
        availableFrom: string,
        availableTo: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players/update_player_availability/me',
            query: {
                'available_from': availableFrom,
                'available_to': availableTo,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Set My Availability
     * @param availabeFrom
     * @param availableTo
     * @returns PlayerAvailability Successful Response
     * @throws ApiError
     */
    public static playersSetMyAvailability(
        availabeFrom: string,
        availableTo: string,
    ): CancelablePromise<PlayerAvailability> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/players/update_player_availability/me',
            query: {
                'availabe_from': availabeFrom,
                'available_to': availableTo,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Player Profile
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersGetMyPlayerProfile(): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_player/me',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Get My Player Rating
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersGetMyPlayerRating(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_player_rating/me',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Get My Player Availabilities
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersGetMyPlayerAvailabilities(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_player_availabilities/me',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Update My Player Profile
     * @param playerHeight
     * @param playerWeight
     * @param playerFoot
     * @param favoritePosition
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersUpdateMyPlayerProfile(
        playerHeight?: number,
        playerWeight?: number,
        playerFoot?: string,
        favoritePosition?: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players/update_player/me',
            query: {
                'player_height': playerHeight,
                'player_weight': playerWeight,
                'player_foot': playerFoot,
                'favorite_position': favoritePosition,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update My Location
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersUpdateMyLocation(): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players/update_player_location/me',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Update My Player Preference
     * @param joinTeam
     * @param joinMatch
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersUpdateMyPlayerPreference(
        joinTeam?: boolean,
        joinMatch?: boolean,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players/update_player_preference/me',
            query: {
                'join_team': joinTeam,
                'join_match': joinMatch,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete My Availability
     * @param availableFrom
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersDeleteMyAvailability(
        availableFrom: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/players/delete_player_availability/me',
            query: {
                'available_from': availableFrom,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete My Availabilities
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersDeleteMyAvailabilities(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/players/delete_player_availabilities/me',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Delete My Player Profile
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersDeleteMyPlayerProfile(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/players/delete_player/me',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Add Coach Request
     * @param coachUsername
     * @param message
     * @param requestDate
     * @param requestTime
     * @param requestExpiryDate
     * @param requestExpiryTime
     * @returns PlayerCoachRequest Successful Response
     * @throws ApiError
     */
    public static playersAddCoachRequest(
        coachUsername: string,
        message?: string,
        requestDate?: string,
        requestTime?: string,
        requestExpiryDate?: string,
        requestExpiryTime?: string,
    ): CancelablePromise<PlayerCoachRequest> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/players/add_coach_request/{coach_username}',
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
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Coach Request
     * @param coachUsername
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersRemoveCoachRequest(
        coachUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/players/remove_coach_request/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Assign My Coach
     * @param coachUsername
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAssignMyCoach(
        coachUsername: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/players/assign_my_coach/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Coach
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static playersGetMyCoach(): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_player_coach/me',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Rate My Coach
     * @param rating
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static playersRateMyCoach(
        rating: number,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players/rate_my_coach/{rating}',
            path: {
                'rating': rating,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove My Coach
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersRemoveMyCoach(): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/players/remove_my_coach',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Player Teams
     * @returns TeamPlayerLink Successful Response
     * @throws ApiError
     */
    public static playersPlayerTeams(): CancelablePromise<Array<TeamPlayerLink>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_my_teams',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Add Team Request
     * @param teamName
     * @param message
     * @param requestDate
     * @param requestTime
     * @param requestExpiryDate
     * @param requestExpiryTime
     * @returns PlayerTeamRequest Successful Response
     * @throws ApiError
     */
    public static playersAddTeamRequest(
        teamName: string,
        message?: string,
        requestDate?: string,
        requestTime?: string,
        requestExpiryDate?: string,
        requestExpiryTime?: string,
    ): CancelablePromise<PlayerTeamRequest> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/players/add_team_request/{team_name}',
            path: {
                'team_name': teamName,
            },
            query: {
                'message': message,
                'request_date': requestDate,
                'request_time': requestTime,
                'request_expiry_date': requestExpiryDate,
                'request_expiry_time': requestExpiryTime,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Team Request
     * @param teamName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersRemoveTeamRequest(
        teamName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/players/remove_team_request/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Teams Invitations
     * @returns PlayerTeamInvitation Successful Response
     * @throws ApiError
     */
    public static playersGetMyTeamsInvitations(): CancelablePromise<Array<PlayerTeamInvitation>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_team_invitations/{team_name}',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Get Player Invitation
     * @param teamName
     * @returns PlayerTeamInvitation Successful Response
     * @throws ApiError
     */
    public static playersGetPlayerInvitation(
        teamName: string,
    ): CancelablePromise<PlayerTeamInvitation> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_player_invitation/{team_name}/me',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update My Team Invitation
     * @param teamName
     * @param isAccepted
     * @returns PlayerTeamInvitation Successful Response
     * @throws ApiError
     */
    public static playersUpdateMyTeamInvitation(
        teamName: string,
        isAccepted: boolean,
    ): CancelablePromise<Array<PlayerTeamInvitation>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players/update_player_team_invitation/me',
            query: {
                'team_name': teamName,
                'is_accepted': isAccepted,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Assign Me To Team
     * @param teamName
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAssignMeToTeam(
        teamName: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/players/assign_me_to_team/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Rate My Team
     * @param teamName
     * @param rating
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static playersRateMyTeam(
        teamName: string,
        rating: number,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players/rate_my_team/{team_name}/{rating}',
            path: {
                'team_name': teamName,
                'rating': rating,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove My Team
     * @param teamName
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersRemoveMyTeam(
        teamName: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/players/remove_me_from_team/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Player Captain Teams
     * @returns TeamPlayerLink Successful Response
     * @throws ApiError
     */
    public static playersGetPlayerCaptainTeams(): CancelablePromise<Array<TeamPlayerLink>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_player_captain_teams/me',
            errors: {
                404: `Players Not found`,
            },
        });
    }

    /**
     * Remove Team Captain
     * @param teamName
     * @returns TeamPlayerLink Successful Response
     * @throws ApiError
     */
    public static playersRemoveTeamCaptain(
        teamName: string,
    ): CancelablePromise<TeamPlayerLink> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players/remove_me_as_team_captain/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Players By Radius
     * @param radius
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersFindPlayersByRadius(
        radius: number,
    ): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/find_players_by_radius/{radius}',
            path: {
                'radius': radius,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Players By Position In My Radius
     * @param favoritePosition
     * @param radius
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersFindPlayersByPositionInMyRadius(
        favoritePosition: string,
        radius: number,
    ): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/find_players_by_position_radius/{favorite_position}/{radius}',
            path: {
                'favorite_position': favoritePosition,
                'radius': radius,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Players By Rating In My Radius
     * @param rating
     * @param radius
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersFindPlayersByRatingInMyRadius(
        rating: number,
        radius: number,
    ): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/find_players_by_rating_radius/{rating}/{radius}',
            path: {
                'rating': rating,
                'radius': radius,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Player Rating
     * @param playerUsername
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersGetPlayerRating(
        playerUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_player_rating/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Players By Rating
     * @param rating
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersFindPlayersByRating(
        rating: number,
    ): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players/get_players_by_rating/{rating}',
            path: {
                'rating': rating,
            },
            errors: {
                404: `Players Not found`,
                422: `Validation Error`,
            },
        });
    }

}
