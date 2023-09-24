/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StadiumRead } from '../models/StadiumRead';
import type { TeamRead } from '../models/TeamRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StadiumTeamsService {

    /**
     * Get Team Home Stadium
     * @param teamName
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumTeamsGetTeamHomeStadium(
        teamName: string,
    ): CancelablePromise<StadiumRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadium_teams/get_team_home_stadium/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Stadium team Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Teams By Home Stadium
     * @param stadiumName
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static stadiumTeamsGetTeamsByHomeStadium(
        stadiumName: string,
    ): CancelablePromise<Array<TeamRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadium_teams/get_teams_by_home_stadium/{stadium_name}',
            path: {
                'stadium_name': stadiumName,
            },
            errors: {
                404: `Stadium team Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Stadium Home Teams
     * @param stadiumName
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static stadiumTeamsGetStadiumHomeTeams(
        stadiumName: string,
    ): CancelablePromise<Array<TeamRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadium_teams/get_stadium_home_teams/{stadium_name}',
            path: {
                'stadium_name': stadiumName,
            },
            errors: {
                404: `Stadium team Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Team Home Stadium
     * @param teamName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static stadiumTeamsRemoveTeamHomeStadium(
        teamName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/stadium_teams/remove_team_home_stadium/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Stadium team Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Assign Team Home Stadium
     * @param teamName
     * @param stadiumId
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static stadiumTeamsAssignTeamHomeStadium(
        teamName: string,
        stadiumId: number,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/stadium_teams/assign_team_home_stadium/{team_name}/{stadium_name}',
            path: {
                'team_name': teamName,
            },
            query: {
                'stadium_id': stadiumId,
            },
            errors: {
                404: `Stadium team Not found`,
                422: `Validation Error`,
            },
        });
    }

}
