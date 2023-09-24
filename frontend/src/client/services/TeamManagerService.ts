/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ManagerRead } from '../models/ManagerRead';
import type { TeamRead } from '../models/TeamRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class TeamManagerService {

    /**
     * Get All Team Managers
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static teamManagerGetAllTeamManagers(): CancelablePromise<Array<ManagerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/team_manager/get_teams_managers',
            errors: {
                418: `I'm an Administrator`,
            },
        });
    }

    /**
     * Read Team Manager
     * @param teamName
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static teamManagerReadTeamManager(
        teamName: string,
    ): CancelablePromise<ManagerRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/team_manager/get_team_manager/{team_name}',
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
     * Read Manager Teams
     * @param managerUsername
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamManagerReadManagerTeams(
        managerUsername: string,
    ): CancelablePromise<Array<TeamRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/team_manager/get_manager_teams/{manager_username}',
            path: {
                'manager_username': managerUsername,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Assign New Team Manager
     * @param teamName
     * @param username
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamManagerAssignNewTeamManager(
        teamName: string,
        username: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/team_manager/assign_team_manager/{team_name}/{username}',
            path: {
                'team_name': teamName,
                'username': username,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Manager From Team
     * @param teamName
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamManagerRemoveManagerFromTeam(
        teamName: string,
    ): CancelablePromise<TeamRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/team_manager/remove_team_manager/{team_name}',
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
     * Manager Rating
     * @param teamName
     * @param managerRating
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static teamManagerManagerRating(
        teamName: string,
        managerRating: number,
    ): CancelablePromise<ManagerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/team_manager/manager_rating/{team_name}/{manager_rating}',
            path: {
                'team_name': teamName,
                'manager_rating': managerRating,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

}
