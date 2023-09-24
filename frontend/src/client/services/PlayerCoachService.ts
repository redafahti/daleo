/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CoachRead } from '../models/CoachRead';
import type { PlayerRead } from '../models/PlayerRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PlayerCoachService {

    /**
     * Read All Players Coaches
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static playerCoachReadAllPlayersCoaches(): CancelablePromise<Array<CoachRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/player_coach/get_all_players_coaches',
            errors: {
                404: `Player Coach Not found`,
            },
        });
    }

    /**
     * Read Coach Players
     * @param coachUsername
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playerCoachReadCoachPlayers(
        coachUsername: string,
    ): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/player_coach/get_coach_players/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Player Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Player Coach
     * @param playerUsername
     * @returns CoachRead Successful Response
     * @throws ApiError
     */
    public static playerCoachReadPlayerCoach(
        playerUsername: string,
    ): CancelablePromise<CoachRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/player_coach/get_player_coach/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            errors: {
                404: `Player Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Assign Coach To Player
     * @param playerUsername
     * @param coachUsername
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playerCoachAssignCoachToPlayer(
        playerUsername: string,
        coachUsername: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/player_coach/assign_coach_to_player/{player_username}/{coach_username}',
            path: {
                'player_username': playerUsername,
                'coach_username': coachUsername,
            },
            errors: {
                404: `Player Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Player From Coach
     * @param playerUsername
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playerCoachRemovePlayerFromCoach(
        playerUsername: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/player_coach/remove_player_coach/me',
            query: {
                'player_username': playerUsername,
            },
            errors: {
                404: `Player Coach Not found`,
                422: `Validation Error`,
            },
        });
    }

}
