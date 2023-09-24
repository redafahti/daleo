/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MatchPlayerLink } from '../models/MatchPlayerLink';
import type { PlayerMatchInvitation } from '../models/PlayerMatchInvitation';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class MatchPlayersService {

    /**
     * Read Player Matches
     * @param username
     * @returns MatchPlayerLink Successful Response
     * @throws ApiError
     */
    public static matchPlayersReadPlayerMatches(
        username: string,
    ): CancelablePromise<Array<MatchPlayerLink>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_players/get_player_matches/{username}',
            path: {
                'username': username,
            },
            errors: {
                404: `Match player Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Player Match
     * @param matchId
     * @param username
     * @returns MatchPlayerLink Successful Response
     * @throws ApiError
     */
    public static matchPlayersReadPlayerMatch(
        matchId: number,
        username: string,
    ): CancelablePromise<MatchPlayerLink> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_players/get_player_match/{match_id}/{username}',
            path: {
                'match_id': matchId,
                'username': username,
            },
            errors: {
                404: `Match player Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Player Match Invitation
     * @param playerName
     * @param matchId
     * @param invitationDate
     * @param invitationTime
     * @param invitationExpiryDate
     * @param invitationExpiryTime
     * @returns PlayerMatchInvitation Successful Response
     * @throws ApiError
     */
    public static matchPlayersCreatePlayerMatchInvitation(
        playerName: string,
        matchId: number,
        invitationDate?: string,
        invitationTime?: string,
        invitationExpiryDate?: string,
        invitationExpiryTime?: string,
    ): CancelablePromise<PlayerMatchInvitation> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/match_players/create_player_match_invitation/{player_name}/{match_id}',
            path: {
                'player_name': playerName,
                'match_id': matchId,
            },
            query: {
                'invitation_date': invitationDate,
                'invitation_time': invitationTime,
                'invitation_expiry_date': invitationExpiryDate,
                'invitation_expiry_time': invitationExpiryTime,
            },
            errors: {
                404: `Match player Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Player Match Invitation
     * @param playerName
     * @param matchId
     * @returns PlayerMatchInvitation Successful Response
     * @throws ApiError
     */
    public static matchPlayersReadPlayerMatchInvitation(
        playerName: string,
        matchId: number,
    ): CancelablePromise<PlayerMatchInvitation> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_players/get_player_match_invitation',
            query: {
                'player_name': playerName,
                'match_id': matchId,
            },
            errors: {
                404: `Match player Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Player Match Invitations By Player Id
     * @param playerName
     * @returns PlayerMatchInvitation Successful Response
     * @throws ApiError
     */
    public static matchPlayersGetPlayerMatchInvitationsByPlayerId(
        playerName: string,
    ): CancelablePromise<Array<PlayerMatchInvitation>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_players/get_player_match_invitations/{player_name}',
            path: {
                'player_name': playerName,
            },
            errors: {
                404: `Match player Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Player Match Invitations By Match Id
     * @param matchId
     * @returns PlayerMatchInvitation Successful Response
     * @throws ApiError
     */
    public static matchPlayersGetPlayerMatchInvitationsByMatchId(
        matchId: number,
    ): CancelablePromise<Array<PlayerMatchInvitation>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/match_players/get_player_match_invitations_by_match_id/{match_id}',
            path: {
                'match_id': matchId,
            },
            errors: {
                404: `Match player Not found`,
                422: `Validation Error`,
            },
        });
    }

}
