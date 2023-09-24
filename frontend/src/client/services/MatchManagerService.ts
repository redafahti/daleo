/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MatchTeamLink } from '../models/MatchTeamLink';
import type { PlayerTeamRequest } from '../models/PlayerTeamRequest';
import type { TeamMatchRequest } from '../models/TeamMatchRequest';
import type { TeamPlayerLink } from '../models/TeamPlayerLink';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class MatchManagerService {

    /**
     * New Match
     * @param teamName
     * @param stadiumId
     * @param matchDuration
     * @param matchStartTime
     * @param teamsSize
     * @param numberOfSubstitutes
     * @param matchType
     * @param matchPrize
     * @returns MatchTeamLink Successful Response
     * @throws ApiError
     */
    public static matchManagerNewMatch(
        teamName: string,
        stadiumId: number,
        matchDuration: number,
        matchStartTime: string,
        teamsSize: number,
        numberOfSubstitutes?: number,
        matchType?: string,
        matchPrize?: number,
    ): CancelablePromise<MatchTeamLink> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/match_manager/create_match',
            query: {
                'team_name': teamName,
                'stadium_id': stadiumId,
                'match_duration': matchDuration,
                'match_start_time': matchStartTime,
                'teams_size': teamsSize,
                'number_of_substitutes': numberOfSubstitutes,
                'match_type': matchType,
                'match_prize': matchPrize,
            },
            errors: {
                404: `Match Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Team Requests
     * @param teamName
     * @returns TeamMatchRequest Successful Response
     * @throws ApiError
     */
    public static matchManagerReadTeamRequests(
        teamName: string,
    ): CancelablePromise<Array<TeamMatchRequest>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_manager/get_team_requests/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Match Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Player Request
     * @param playerUsername
     * @param teamName
     * @param isAccepted
     * @returns PlayerTeamRequest Successful Response
     * @throws ApiError
     */
    public static matchManagerUpdatePlayerRequest(
        playerUsername: string,
        teamName: string,
        isAccepted: boolean,
    ): CancelablePromise<PlayerTeamRequest> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/match_manager/update_player_request/{player_username}/{team_name}/{is_accepted}',
            path: {
                'player_username': playerUsername,
                'team_name': teamName,
                'is_accepted': isAccepted,
            },
            errors: {
                404: `Match Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Assign Player To Team
     * @param playerUsername
     * @param teamName
     * @param isCaptain
     * @param playerPosition
     * @returns TeamPlayerLink Successful Response
     * @throws ApiError
     */
    public static matchManagerAssignPlayerToTeam(
        playerUsername: string,
        teamName: string,
        isCaptain: boolean = false,
        playerPosition?: string,
    ): CancelablePromise<TeamPlayerLink> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/match_manager/add_team/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            query: {
                'team_name': teamName,
                'is_captain': isCaptain,
                'player_position': playerPosition,
            },
            errors: {
                404: `Match Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Team
     * @param teamName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static matchManagerRemoveTeam(
        teamName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/match_manager/remove_team/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Match Managers Not found`,
                422: `Validation Error`,
            },
        });
    }

}
