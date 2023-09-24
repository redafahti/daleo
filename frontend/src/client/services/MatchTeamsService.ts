/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MatchRead } from '../models/MatchRead';
import type { TeamMatchInvitation } from '../models/TeamMatchInvitation';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class MatchTeamsService {

    /**
     * Get Team Matches
     * @param teamName
     * @returns MatchRead Successful Response
     * @throws ApiError
     */
    public static matchTeamsGetTeamMatches(
        teamName: string,
    ): CancelablePromise<Array<MatchRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_teams/get_team_matches/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Match Teams Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * New Team Match Invitation
     * @param teamName
     * @param matchId
     * @param invitationDate
     * @param invitationTime
     * @param invitationExpiryDate
     * @param invitationExpiryTime
     * @returns TeamMatchInvitation Successful Response
     * @throws ApiError
     */
    public static matchTeamsNewTeamMatchInvitation(
        teamName: string,
        matchId: number,
        invitationDate?: string,
        invitationTime?: string,
        invitationExpiryDate?: string,
        invitationExpiryTime?: string,
    ): CancelablePromise<TeamMatchInvitation> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/match_teams/create_team_match_invitation/{team_name}/{match_id}',
            path: {
                'team_name': teamName,
                'match_id': matchId,
            },
            query: {
                'invitation_date': invitationDate,
                'invitation_time': invitationTime,
                'invitation_expiry_date': invitationExpiryDate,
                'invitation_expiry_time': invitationExpiryTime,
            },
            errors: {
                404: `Match Teams Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Team Match Invitation
     * @param teamName
     * @param matchId
     * @returns TeamMatchInvitation Successful Response
     * @throws ApiError
     */
    public static matchTeamsReadTeamMatchInvitation(
        teamName: string,
        matchId: number,
    ): CancelablePromise<TeamMatchInvitation> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_teams/get_team_match_invitation',
            query: {
                'team_name': teamName,
                'match_id': matchId,
            },
            errors: {
                404: `Match Teams Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Team Match Invitations
     * @param teamName
     * @returns TeamMatchInvitation Successful Response
     * @throws ApiError
     */
    public static matchTeamsReadTeamMatchInvitations(
        teamName: string,
    ): CancelablePromise<Array<TeamMatchInvitation>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_teams/get_team_match_invitations/{team_name}',
            path: {
                'team_name': teamName,
            },
            errors: {
                404: `Match Teams Not found`,
                422: `Validation Error`,
            },
        });
    }

}
