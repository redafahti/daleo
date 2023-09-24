/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TeamRead } from '../models/TeamRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class TeamsAdminService {

    /**
     * Get All Teams
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamsAdminGetAllTeams(): CancelablePromise<Array<TeamRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/teams_admin/get_teams',
            errors: {
                418: `I'm an Administrator`,
            },
        });
    }

    /**
     * Read Team
     * @param teamName
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamsAdminReadTeam(
        teamName: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/teams_admin/get_team/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Team Update
     * @param teamName
     * @param teamLogo
     * @param teamHomeColorJersey
     * @param teamAwayColorJersey
     * @param teamHomeColorShorts
     * @param teamAwayColorShorts
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamsAdminTeamUpdate(
        teamName: string,
        teamLogo?: string,
        teamHomeColorJersey?: string,
        teamAwayColorJersey?: string,
        teamHomeColorShorts?: string,
        teamAwayColorShorts?: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/teams_admin/update_team/{team_name}',
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
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Team Rating Update
     * @param teamName
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamsAdminTeamRatingUpdate(
        teamName: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/teams_admin/update_team_rating/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Team Delete
     * @param teamName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static teamsAdminTeamDelete(
        teamName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/teams_admin/delete_team/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

}
