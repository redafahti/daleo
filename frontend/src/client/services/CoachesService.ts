/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CoachRead } from '../models/CoachRead';
import type { PlayerCoachRequest } from '../models/PlayerCoachRequest';
import type { PlayerRead } from '../models/PlayerRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class CoachesService {

    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static coachesReadRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/',
            errors: {
                404: `Coach Not found`,
            },
        });
    }

    /**
     * Create My Coach Profile
     * @param coachPlayerHourlyRate
     * @param coachTeamHourlyRate
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesCreateMyCoachProfile(
        coachPlayerHourlyRate?: number,
        coachTeamHourlyRate?: number,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/coaches/create_coach/me',
            query: {
                'coach_player_hourly_rate': coachPlayerHourlyRate,
                'coach_team_hourly_rate': coachTeamHourlyRate,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get My Coach Profile
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesGetMyCoachProfile(): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/get_coach/me',
            errors: {
                404: `Coach Not found`,
            },
        });
    }

    /**
     * Update My Coach Profile
     * @param coachHourlyRate
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesUpdateMyCoachProfile(
        coachHourlyRate?: number,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/coaches/update_coach/me',
            query: {
                'coach_hourly_rate': coachHourlyRate,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update My Location
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesUpdateMyLocation(): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/coaches/update_coach_location/me',
            errors: {
                404: `Coach Not found`,
            },
        });
    }

    /**
     * Get My Coach Rating
     * @returns any Successful Response
     * @throws ApiError
     */
    public static coachesGetMyCoachRating(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/get_coach_rating/me',
            errors: {
                404: `Coach Not found`,
            },
        });
    }

    /**
     * Get My Players
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static coachesGetMyPlayers(): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/get_coach_players/me',
            errors: {
                404: `Coach Not found`,
            },
        });
    }

    /**
     * Get My Players Coach Requests
     * @returns PlayerCoachRequest Successful Response
     * @throws ApiError
     */
    public static coachesGetMyPlayersCoachRequests(): CancelablePromise<Array<PlayerCoachRequest>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/get_coach_players_requests/me',
            errors: {
                404: `Coach Not found`,
            },
        });
    }

    /**
     * Update My Player Coach Request
     * @param playerUsername
     * @param isAccepted
     * @returns PlayerCoachRequest Successful Response
     * @throws ApiError
     */
    public static coachesUpdateMyPlayerCoachRequest(
        playerUsername: string,
        isAccepted: boolean,
    ): CancelablePromise<PlayerCoachRequest> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/coaches/update_player_coach_request/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            query: {
                'is_accepted': isAccepted,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete My Coach Profile
     * @returns any Successful Response
     * @throws ApiError
     */
    public static coachesDeleteMyCoachProfile(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/coaches/delete_coach/me',
            errors: {
                404: `Coach Not found`,
            },
        });
    }

    /**
     * Get Coach Profile
     * @param coachUsername
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesGetCoachProfile(
        coachUsername: string,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/get_coach/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Coach Rating
     * @param coachUsername
     * @returns any Successful Response
     * @throws ApiError
     */
    public static coachesGetCoachRating(
        coachUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/get_coach_rating/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Coaches By Location
     * @param radius
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesFindCoachesByLocation(
        radius: number,
    ): CancelablePromise<Array<CoachRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/find_coaches_by_location/{radius}',
            path: {
                'radius': radius,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Coaches By Stadium
     * @param stadiumId
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesFindCoachesByStadium(
        stadiumId: number,
    ): CancelablePromise<Array<CoachRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/find_coaches_by_stadium/{stadium_id}',
            path: {
                'stadium_id': stadiumId,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Coaches By Rating
     * @param rating
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesFindCoachesByRating(
        rating: number,
    ): CancelablePromise<Array<CoachRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches/find_coaches_by_rating/{rating}',
            path: {
                'rating': rating,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

}
