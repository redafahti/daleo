/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TeamRead } from '../models/TeamRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class TeamsService {

    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static teamsReadRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/teams/',
            errors: {
                404: `Team Not found`,
            },
        });
    }

    /**
     * Read Team
     * @param teamName
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamsReadTeam(
        teamName: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/teams/get_team/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Team Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Team Rating
     * @param teamName
     * @returns number Successful Response
     * @throws ApiError
     */
    public static teamsReadTeamRating(
        teamName: string,
    ): CancelablePromise<number> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/teams/get_team_rating/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Team Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Teams By Stadium
     * @param stadiumId
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamsFindTeamsByStadium(
        stadiumId: number,
    ): CancelablePromise<Array<TeamRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/teams/find_teams_by_stadium/{stadium_id}',
            path: {
                'stadium_id': stadiumId,
            },
            errors: {
                404: `Team Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Teams By Rating
     * @param rating
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamsFindTeamsByRating(
        rating: number,
    ): CancelablePromise<Array<TeamRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/teams/find_teams_by_rating/{rating}',
            path: {
                'rating': rating,
            },
            errors: {
                404: `Team Not found`,
                422: `Validation Error`,
            },
        });
    }

}
