/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MatchRead } from '../models/MatchRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class MatchesAdminService {

    /**
     * All Matches
     * @returns MatchRead Successful Response
     * @throws ApiError
     */
    public static matchesAdminAllMatches(): CancelablePromise<Array<MatchRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/matches_admin/get_matches',
            errors: {
                404: `Match Not found`,
            },
        });
    }

    /**
     * Read Match
     * @param matchId
     * @returns MatchRead Successful Response
     * @throws ApiError
     */
    public static matchesAdminReadMatch(
        matchId: number,
    ): CancelablePromise<MatchRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/matches_admin/get_match/{match_id}',
            path: {
                'match_id': matchId,
            },
            errors: {
                404: `Match Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Match Update
     * @param matchId
     * @param homeTeamName
     * @param awayTeamName
     * @param matchDuration
     * @param matchStartTime
     * @param matchEndTime
     * @param stadiumName
     * @param isBooked
     * @param bookingConfirmed
     * @param matchStatus
     * @param matchType
     * @param matchPrize
     * @returns any Successful Response
     * @throws ApiError
     */
    public static matchesAdminMatchUpdate(
        matchId: number,
        homeTeamName?: string,
        awayTeamName?: string,
        matchDuration?: number,
        matchStartTime?: string,
        matchEndTime?: string,
        stadiumName?: string,
        isBooked?: boolean,
        bookingConfirmed?: boolean,
        matchStatus?: string,
        matchType?: string,
        matchPrize?: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/matches_admin/update_match/{match_id}',
            path: {
                'match_id': matchId,
            },
            query: {
                'home_team_name': homeTeamName,
                'away_team_name': awayTeamName,
                'match_duration': matchDuration,
                'match_start_time': matchStartTime,
                'match_end_time': matchEndTime,
                'stadium_name': stadiumName,
                'is_booked': isBooked,
                'booking_confirmed': bookingConfirmed,
                'match_status': matchStatus,
                'match_type': matchType,
                'match_prize': matchPrize,
            },
            errors: {
                404: `Match Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Match Delete
     * @param matchId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static matchesAdminMatchDelete(
        matchId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/matches_admin/delete_match/{match_id}',
            path: {
                'match_id': matchId,
            },
            errors: {
                404: `Match Not found`,
                422: `Validation Error`,
            },
        });
    }

}
