/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MatchRead } from '../models/MatchRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class MatchRefereeService {

    /**
     * Read Referee Matches
     * @param username
     * @returns MatchRead Successful Response
     * @throws ApiError
     */
    public static matchRefereeReadRefereeMatches(
        username: string,
    ): CancelablePromise<Array<MatchRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_referee/get_referee_matches/{username}',
            path: {
                'username': username,
            },
            errors: {
                404: `Match referee Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Referee To Match
     * @param matchId
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static matchRefereeAddRefereeToMatch(
        matchId: number,
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/match_referee/add_referee_to_match/{match_id}/{username}',
            path: {
                'match_id': matchId,
                'username': username,
            },
            errors: {
                404: `Match referee Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Referee From Match
     * @param matchId
     * @param refereeUsername
     * @returns any Successful Response
     * @throws ApiError
     */
    public static matchRefereeRemoveRefereeFromMatch(
        matchId: number,
        refereeUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/match_referee/remove_referee_from_match/{match_id}/{username}',
            path: {
                'match_id': matchId,
            },
            query: {
                'referee_username': refereeUsername,
            },
            errors: {
                404: `Match referee Not found`,
                422: `Validation Error`,
            },
        });
    }

}
