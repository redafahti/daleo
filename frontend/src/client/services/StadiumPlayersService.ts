/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TeamRead } from '../models/TeamRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StadiumPlayersService {

    /**
     * Find Teams By Location
     * @param radius
     * @param username
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static stadiumPlayersFindTeamsByLocation(
        radius: number,
        username: string,
    ): CancelablePromise<Array<TeamRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadium_players/find_team_by_location/{radius}',
            path: {
                'radius': radius,
            },
            query: {
                'username': username,
            },
            errors: {
                404: `Stadium players Not found`,
                422: `Validation Error`,
            },
        });
    }

}
