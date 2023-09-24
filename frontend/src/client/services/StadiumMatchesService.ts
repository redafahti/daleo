/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MatchRead } from '../models/MatchRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StadiumMatchesService {

    /**
     * Find Stadium Matches
     * @param stadiumName
     * @returns MatchRead Successful Response
     * @throws ApiError
     */
    public static stadiumMatchesFindStadiumMatches(
        stadiumName: string,
    ): CancelablePromise<Array<MatchRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadium_matches/get_stadium_matches/{stadium_name}',
            path: {
                'stadium_name': stadiumName,
            },
            errors: {
                404: `Stadium match Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Stadium Matches By Date
     * @param stadiumName
     * @param startDate
     * @param endDate
     * @returns MatchRead Successful Response
     * @throws ApiError
     */
    public static stadiumMatchesGetStadiumMatchesByDate(
        stadiumName: string,
        startDate: string,
        endDate: string,
    ): CancelablePromise<Array<MatchRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadium_matches/get_stadium_matches_by_date/{stadium_name}/{start_date}/{end_date}',
            path: {
                'stadium_name': stadiumName,
                'start_date': startDate,
                'end_date': endDate,
            },
            errors: {
                404: `Stadium match Not found`,
                422: `Validation Error`,
            },
        });
    }

}
