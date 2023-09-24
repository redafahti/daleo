/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Stadium } from '../models/Stadium';
import type { StadiumRead } from '../models/StadiumRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StadiumsAdminService {

    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static stadiumsAdminReadRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadiums_admin/',
            errors: {
                404: `stadium Not found`,
            },
        });
    }

    /**
     * Get Stadiums
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumsAdminGetStadiums(): CancelablePromise<Array<StadiumRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadiums_admin/get_stadiums',
            errors: {
                404: `stadium Not found`,
            },
        });
    }

    /**
     * New Stadium
     * @param stadiumName
     * @param stadiumPitches
     * @param stadiumContact
     * @param stadiumEmail
     * @param stadiumMobile
     * @param stadiumLongitude
     * @param stadiumLatitude
     * @param stadiumNeighborhood
     * @param stadiumCity
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumsAdminNewStadium(
        stadiumName: string,
        stadiumPitches: number,
        stadiumContact?: string,
        stadiumEmail?: string,
        stadiumMobile?: string,
        stadiumLongitude?: number,
        stadiumLatitude?: number,
        stadiumNeighborhood?: string,
        stadiumCity?: string,
    ): CancelablePromise<StadiumRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/stadiums_admin/create_stadium/{stadium_name}',
            path: {
                'stadium_name': stadiumName,
            },
            query: {
                'stadium_pitches': stadiumPitches,
                'stadium_contact': stadiumContact,
                'stadium_email': stadiumEmail,
                'stadium_mobile': stadiumMobile,
                'stadium_longitude': stadiumLongitude,
                'stadium_latitude': stadiumLatitude,
                'stadium_neighborhood': stadiumNeighborhood,
                'stadium_city': stadiumCity,
            },
            errors: {
                404: `stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Stadium Update
     * @param stadiumId
     * @param stadiumName
     * @param stadiumPitches
     * @param bookedPitches
     * @param confirmedBookings
     * @param stadiumContact
     * @param stadiumEmail
     * @param stadiumMobile
     * @param stadiumLongitude
     * @param stadiumLatitude
     * @param stadiumNeighborhood
     * @param stadiumCity
     * @param stadiumRating
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumsAdminStadiumUpdate(
        stadiumId: number,
        stadiumName?: string,
        stadiumPitches?: number,
        bookedPitches?: number,
        confirmedBookings?: number,
        stadiumContact?: string,
        stadiumEmail?: string,
        stadiumMobile?: string,
        stadiumLongitude?: number,
        stadiumLatitude?: number,
        stadiumNeighborhood?: string,
        stadiumCity?: string,
        stadiumRating?: number,
    ): CancelablePromise<StadiumRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/stadiums_admin/update_stadium/{stadium_id}',
            path: {
                'stadium_id': stadiumId,
            },
            query: {
                'stadium_name': stadiumName,
                'stadium_pitches': stadiumPitches,
                'booked_pitches': bookedPitches,
                'confirmed_bookings': confirmedBookings,
                'stadium_contact': stadiumContact,
                'stadium_email': stadiumEmail,
                'stadium_mobile': stadiumMobile,
                'stadium_longitude': stadiumLongitude,
                'stadium_latitude': stadiumLatitude,
                'stadium_neighborhood': stadiumNeighborhood,
                'stadium_city': stadiumCity,
                'stadium_rating': stadiumRating,
            },
            errors: {
                404: `stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Stadium
     * @param stadiumName
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumsAdminReadStadium(
        stadiumName: string,
    ): CancelablePromise<StadiumRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadiums_admin/get_stadium/{stadium_name}',
            path: {
                'stadium_name': stadiumName,
            },
            errors: {
                404: `stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Google Stadium By City
     * @param city
     * @returns any Successful Response
     * @throws ApiError
     */
    public static stadiumsAdminReadGoogleStadiumByCity(
        city: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadiums_admin/get_google_city_stadiums/{city}',
            path: {
                'city': city,
            },
            errors: {
                404: `stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Google Stadium By Place Id
     * @param placeId
     * @returns StadiumRead Successful Response
     * @throws ApiError
     */
    public static stadiumsAdminReadGoogleStadiumByPlaceId(
        placeId: string,
    ): CancelablePromise<StadiumRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadiums_admin/get_stadium_by_place_id/{place_id}',
            path: {
                'place_id': placeId,
            },
            errors: {
                404: `stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Stadiums From Google By City
     * @param city
     * @returns Stadium Successful Response
     * @throws ApiError
     */
    public static stadiumsAdminAddStadiumsFromGoogleByCity(
        city: string,
    ): CancelablePromise<Array<Stadium>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/stadiums_admin/add_google_city_stadiums/{city}',
            path: {
                'city': city,
            },
            errors: {
                404: `stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Stadium Delete
     * @param stadiumName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static stadiumsAdminStadiumDelete(
        stadiumName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/stadiums_admin/delete_stadium/{stadium_name}',
            path: {
                'stadium_name': stadiumName,
            },
            errors: {
                404: `stadium Not found`,
                422: `Validation Error`,
            },
        });
    }

}
