/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PlayerRead } from '../models/PlayerRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PlayersAdminService {

    /**
     * Get All Players
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAdminGetAllPlayers(): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players_admin/get_players',
            errors: {
                418: `I'm an Administrator`,
            },
        });
    }

    /**
     * Create New Player
     * @param username
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAdminCreateNewPlayer(
        username: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/players_admin/create_player/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Player Profile
     * @param playerUsername
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAdminGetPlayerProfile(
        playerUsername: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players_admin/get_player/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Players By Radius
     * @param longitude
     * @param latitude
     * @param radius
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAdminFindPlayersByRadius(
        longitude: number,
        latitude: number,
        radius: number,
    ): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players_admin/find_players_by_radius/{longitude}/{latitude}/{radius}',
            path: {
                'longitude': longitude,
                'latitude': latitude,
                'radius': radius,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Players By Position In My Radius
     * @param favoritePosition
     * @param longitude
     * @param latitude
     * @param radius
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAdminFindPlayersByPositionInMyRadius(
        favoritePosition: string,
        longitude: number,
        latitude: number,
        radius: number,
    ): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players_admin/find_players_by_position_radius/{favorite_position}/{longitude}/{latitude}/{radius}',
            path: {
                'favorite_position': favoritePosition,
                'longitude': longitude,
                'latitude': latitude,
                'radius': radius,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Players By Rating In My Radius
     * @param rating
     * @param longitude
     * @param latitude
     * @param radius
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAdminFindPlayersByRatingInMyRadius(
        rating: number,
        longitude: number,
        latitude: number,
        radius: number,
    ): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players_admin/find_players_by_rating_radius/{rating}/{longitude}/{latitude}/{radius}',
            path: {
                'rating': rating,
                'longitude': longitude,
                'latitude': latitude,
                'radius': radius,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Player Rating
     * @param playerUsername
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersAdminGetPlayerRating(
        playerUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players_admin/get_player_rating/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Players By Rating
     * @param rating
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAdminFindPlayersByRating(
        rating: number,
    ): CancelablePromise<Array<PlayerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/players_admin/get_players_by_rating/{rating}',
            path: {
                'rating': rating,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Player Profile
     * @param playerUsername
     * @param playerHeight
     * @param playerWeight
     * @param playerFoot
     * @param favoritePosition
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAdminUpdatePlayerProfile(
        playerUsername: string,
        playerHeight?: number,
        playerWeight?: number,
        playerFoot?: string,
        favoritePosition?: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players_admin/update_player/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            query: {
                'player_height': playerHeight,
                'player_weight': playerWeight,
                'player_foot': playerFoot,
                'favorite_position': favoritePosition,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Player Rating
     * @param playerUsername
     * @returns PlayerRead Successful Response
     * @throws ApiError
     */
    public static playersAdminUpdatePlayerRating(
        playerUsername: string,
    ): CancelablePromise<PlayerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/players_admin/update_player_rating/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Player Profile
     * @param playerUsername
     * @returns any Successful Response
     * @throws ApiError
     */
    public static playersAdminDeletePlayerProfile(
        playerUsername: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/players_admin/delete_player/{player_username}',
            path: {
                'player_username': playerUsername,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

}
