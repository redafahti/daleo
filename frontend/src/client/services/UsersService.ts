/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_Users_upload_my_photo } from '../models/Body_Users_upload_my_photo';
import type { UserRead } from '../models/UserRead';
import type { UserUpdate } from '../models/UserUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UsersService {

    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersReadRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/',
            errors: {
                404: `User not found`,
            },
        });
    }

    /**
     * Get My User Profile
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static usersGetMyUserProfile(): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/get_user/me',
            errors: {
                404: `User not found`,
            },
        });
    }

    /**
     * Update My User Pofile
     * @param requestBody
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static usersUpdateMyUserPofile(
        requestBody: UserUpdate,
    ): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/user_update/me',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                404: `User not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Upload My Photo
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersUploadMyPhoto(
        formData: Body_Users_upload_my_photo,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/upload_photo/me',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                404: `User not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Is User Player
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersIsUserPlayer(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/user_is_player/me',
            errors: {
                404: `User not found`,
            },
        });
    }

    /**
     * Is User Manager
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersIsUserManager(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/user_is_manager/me',
            errors: {
                404: `User not found`,
            },
        });
    }

    /**
     * Is User Coach
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersIsUserCoach(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/user_is_coach/me',
            errors: {
                404: `User not found`,
            },
        });
    }

    /**
     * Is User Referee
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersIsUserReferee(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/user_is_referee/me',
            errors: {
                404: `User not found`,
            },
        });
    }

    /**
     * Delete My User Profile
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersDeleteMyUserProfile(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/users/user_delete/me',
            errors: {
                404: `User not found`,
            },
        });
    }

}
