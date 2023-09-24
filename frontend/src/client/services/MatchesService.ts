/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MatchPlayerLink } from '../models/MatchPlayerLink';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class MatchesService {

    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static matchesReadRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/matches/',
            errors: {
                404: `Match Not found`,
            },
        });
    }

    /**
     * Rate Team Player
     * @param playerUsername
     * @param teamName
     * @param matchId
     * @param playerRating
     * @returns MatchPlayerLink Successful Response
     * @throws ApiError
     */
    public static matchesRateTeamPlayer(
        playerUsername: string,
        teamName: string,
        matchId: number,
        playerRating: number,
    ): CancelablePromise<Array<MatchPlayerLink>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/matches/rate_team_player/{team_name}/{player_username}',
            path: {
                'player_username': playerUsername,
                'team_name': teamName,
            },
            query: {
                'match_id': matchId,
                'player_rating': playerRating,
            },
            errors: {
                404: `Match Not found`,
                422: `Validation Error`,
            },
        });
    }

}
