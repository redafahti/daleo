/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RefereeRead } from '../models/RefereeRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class RefereesAdminService {

    /**
     * Get All Referees
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesAdminGetAllReferees(): CancelablePromise<Array<RefereeRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees_admin/get_referees',
            errors: {
                404: `Referee Admin Not found`,
            },
        });
    }

    /**
     * Create New Referee
     * @param username
     * @param refereeHourlyRate
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesAdminCreateNewReferee(
        username: string,
        refereeHourlyRate?: number,
    ): CancelablePromise<RefereeRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/referees_admin/create_referee/{username}',
            path: {
                'username': username,
            },
            query: {
                'referee_hourly_rate': refereeHourlyRate,
            },
            errors: {
                404: `Referee Admin Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Referee Profile
     * @param refereeUsername
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesAdminGetRefereeProfile(
        refereeUsername: string,
    ): CancelablePromise<RefereeRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees_admin/get_referee/{referee_username}',
            path: {
                'referee_username': refereeUsername,
            },
            errors: {
                404: `Referee Admin Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Referees In Radius
     * @param longitude
     * @param latitude
     * @param radius
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesAdminFindRefereesInRadius(
        longitude: number,
        latitude: number,
        radius: number,
    ): CancelablePromise<Array<RefereeRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees_admin/find_referees_by_location/{longitude}/{latitude}/{radius}',
            path: {
                'longitude': longitude,
                'latitude': latitude,
                'radius': radius,
            },
            errors: {
                404: `Referee Admin Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Referee Rating
     * @param refereeUsername
     * @returns any Successful Response
     * @throws ApiError
     */
    public static refereesAdminGetRefereeRating(
        refereeUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees_admin/get_referee_rating/{referee_username}',
            path: {
                'referee_username': refereeUsername,
            },
            errors: {
                404: `Referee Admin Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Referees By Rating
     * @param rating
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesAdminFindRefereesByRating(
        rating: number,
    ): CancelablePromise<Array<RefereeRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees_admin/get_referees_by_rating/{rating}',
            path: {
                'rating': rating,
            },
            errors: {
                404: `Referee Admin Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Referee Profile
     * @param refereeUsername
     * @param refereeHourlyRate
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesAdminUpdateRefereeProfile(
        refereeUsername: string,
        refereeHourlyRate?: number,
    ): CancelablePromise<RefereeRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/referees_admin/update_referee/{referee_username}',
            path: {
                'referee_username': refereeUsername,
            },
            query: {
                'referee_hourly_rate': refereeHourlyRate,
            },
            errors: {
                404: `Referee Admin Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Referee Rating
     * @param refereeUsername
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesAdminUpdateRefereeRating(
        refereeUsername: string,
    ): CancelablePromise<RefereeRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/referees_admin/update_referee_rating/{referee_username}',
            path: {
                'referee_username': refereeUsername,
            },
            errors: {
                404: `Referee Admin Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Referee Profile
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static refereesAdminDeleteRefereeProfile(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/referees_admin/delete_referee/{username}',
            path: {
                'username': username,
            },
            errors: {
                404: `Referee Admin Not found`,
                422: `Validation Error`,
            },
        });
    }

}
