/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StadiumRead } from '../models/StadiumRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StadiumsService {

    /**
     * Find Stadiums Within Radius
     * @param radius
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumsFindStadiumsWithinRadius(
        radius: number,
    ): CancelablePromise<Array<StadiumRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadiums/get_stadiums_within_radius/{radius}',
            path: {
                'radius': radius,
            },
            errors: {
                404: `Stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Stadiums By City
     * @param stadiumCity
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumsFindStadiumsByCity(
        stadiumCity: string,
    ): CancelablePromise<Array<StadiumRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadiums/get_stadiums_by_city/{stadium_city}',
            path: {
                'stadium_city': stadiumCity,
            },
            errors: {
                404: `Stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Find Stadiums By Neighborhood
     * @param stadiumNeighborhood
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumsFindStadiumsByNeighborhood(
        stadiumNeighborhood: string,
    ): CancelablePromise<Array<StadiumRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadiums/get_stadiums_by_neighborhood/{stadium_neighborhood}',
            path: {
                'stadium_neighborhood': stadiumNeighborhood,
            },
            errors: {
                404: `Stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Stadium Booked Pitches
     * @param stadiumName
     * @param startTime
     * @param duration
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumsStadiumBookedPitches(
        stadiumName: string,
        startTime: string,
        duration: number,
    ): CancelablePromise<StadiumRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadiums/get_stadium_booked_pitches/{stadium_name}',
            path: {
                'stadium_name': stadiumName,
            },
            query: {
                'start_time': startTime,
                'duration': duration,
            },
            errors: {
                404: `Stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

}
