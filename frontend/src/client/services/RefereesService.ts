/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RefereeRead } from '../models/RefereeRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class RefereesService {

    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static refereesReadRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees/',
            errors: {
                404: `Referee Not found`,
            },
        });
    }

    /**
     * Create My Referee Profile
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesCreateMyRefereeProfile(): CancelablePromise<RefereeRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/referees/create_referee_profile/me',
            errors: {
                404: `Referee Not found`,
            },
        });
    }

    /**
     * Get My Referee Profile
     * @param username
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesGetMyRefereeProfile(
        username: string,
    ): CancelablePromise<RefereeRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees/get_referee_profile/me',
            query: {
                'username': username,
            },
            errors: {
                404: `Referee Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update My Referee Profile
     * @param username
     * @param refereeRating
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesUpdateMyRefereeProfile(
        username: string,
        refereeRating?: number,
    ): CancelablePromise<RefereeRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/referees/update_referee_profile/me',
            query: {
                'username': username,
                'referee_rating': refereeRating,
            },
            errors: {
                404: `Referee Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update My Location
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesUpdateMyLocation(): CancelablePromise<RefereeRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/referees/update_referee_location/me',
            errors: {
                404: `Referee Not found`,
            },
        });
    }

    /**
     * Get My Referee Rating
     * @returns any Successful Response
     * @throws ApiError
     */
    public static refereesGetMyRefereeRating(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees/get_referee_rating/me',
            errors: {
                404: `Referee Not found`,
            },
        });
    }

    /**
     * Delete My Refree Profile
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static refereesDeleteMyRefreeProfile(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/referees/delete_referee_profile/me',
            query: {
                'username': username,
            },
            errors: {
                404: `Referee Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Referees In My Radius
     * @param radius
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesFindRefereesInMyRadius(
        radius: number,
    ): CancelablePromise<Array<RefereeRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees/find_referees_by_radius/{radius}',
            path: {
                'radius': radius,
            },
            errors: {
                404: `Referee Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Referees By Rating In My Radius
     * @param rating
     * @param radius
     * @returns RefereeRead Successful Response
     * @throws ApiError
     */
    public static refereesFindRefereesByRatingInMyRadius(
        rating: number,
        radius: number,
    ): CancelablePromise<Array<RefereeRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/referees/find_referees_by_rating_radius',
            query: {
                'rating': rating,
                'radius': radius,
            },
            errors: {
                404: `Referee Not found`,
                422: `Validation Error`,
            },
        });
    }

}
