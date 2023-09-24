/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CoachRead } from '../models/CoachRead';
import type { PlayerRead } from '../models/PlayerRead';
import type { TeamRead } from '../models/TeamRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class TeamCoachService {

    /**
     * Read Coach Teams
     * @param coachUsername
     * @returns TeamRead Successful Response
     * @throws ApiError
     */
    public static teamCoachReadCoachTeams(
        coachUsername: string,
    ): CancelablePromise<Array<TeamRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/team_coach/get_coach_teams/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Team Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Assign Coach To Team
     * @param coachUsername
     * @param teamName
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static teamCoachAssignCoachToTeam(
        coachUsername: string,
        teamName: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/team_coach/assign_team_coach/{coach_username}/{team_name}',
            path: {
                'coach_username': coachUsername,
                'team_name': teamName,
            },
            errors: {
                404: `Team Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Coach From Team
     * @param teamName
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static teamCoachRemoveCoachFromTeam(
        teamName: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/team_coach/remove_team_coach/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Team Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Team Coach
     * @param teamName
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static teamCoachReadTeamCoach(
        teamName: string,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/team_coach/get_team_coach/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Team Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Rate My Coach
     * @param rating
     * @param teamName
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static teamCoachRateMyCoach(
        rating: number,
        teamName: string,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/team_coach/rate_player_coach/{username}/{rating}',
            path: {
                'rating': rating,
            },
            query: {
                'team_name': teamName,
            },
            errors: {
                404: `Team Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

}
