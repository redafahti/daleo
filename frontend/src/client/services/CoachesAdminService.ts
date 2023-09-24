/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CoachRead } from '../models/CoachRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class CoachesAdminService {

    /**
     * Get All Coaches
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesAdminGetAllCoaches(): CancelablePromise<Array<CoachRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches_admin/get_coaches',
            errors: {
                404: `Coach Not found`,
            },
        });
    }

    /**
     * Create New Coach
     * @param username
     * @param coachPlayerHourlyRate
     * @param coachTeamHourlyRate
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesAdminCreateNewCoach(
        username: string,
        coachPlayerHourlyRate?: number,
        coachTeamHourlyRate?: number,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/coaches_admin/create_coach/{username}',
            path: {
                'username': username,
            },
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
     * Get Coach Profile
     * @param coachUsername
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesAdminGetCoachProfile(
        coachUsername: string,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches_admin/get_coach/{coach_username}',
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
     * Find Coaches In Radius
     * @param longitude
     * @param latitude
     * @param radius
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesAdminFindCoachesInRadius(
        longitude: number,
        latitude: number,
        radius: number,
    ): CancelablePromise<Array<CoachRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches_admin/find_coaches_by_location/{longitude}/{latitude}/{radius}',
            path: {
                'longitude': longitude,
                'latitude': latitude,
                'radius': radius,
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
    public static coachesAdminGetCoachRating(
        coachUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches_admin/get_coach_rating/{coach_username}',
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
     * Find Coaches By Rating
     * @param rating
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesAdminFindCoachesByRating(
        rating: number,
    ): CancelablePromise<Array<CoachRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coaches_admin/get_coaches_by_rating/{rating}',
            path: {
                'rating': rating,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Coach Profile
     * @param coachUsername
     * @param coachPlayerHourlyRate
     * @param coachTeamHourlyRate
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesAdminUpdateCoachProfile(
        coachUsername: string,
        coachPlayerHourlyRate?: number,
        coachTeamHourlyRate?: number,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/coaches_admin/update_coach/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
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
     * Update Coach Rating
     * @param coachUsername
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static coachesAdminUpdateCoachRating(
        coachUsername: string,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/coaches_admin/update_coach_rating/{coach_username}',
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
     * Delete Coach Profile
     * @param coachUsername
     * @returns any Successful Response
     * @throws ApiError
     */
    public static coachesAdminDeleteCoachProfile(
        coachUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/coaches_admin/delete_coach/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

}
