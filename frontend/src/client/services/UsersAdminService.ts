/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UserRead } from '../models/UserRead';
import type { UserUpdate } from '../models/UserUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UsersAdminService {

    /**
     * Get All Users
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static usersAdminGetAllUsers(): CancelablePromise<Array<UserRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users_admin/all_users',
            errors: {
                418: `I'm a User Administrator`,
            },
        });
    }

    /**
     * Get User Profile
     * @param username
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static usersAdminGetUserProfile(
        username: string,
    ): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users_admin/get_user/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * New User
     * @param username
     * @param password
     * @param email
     * @param mobile
     * @param userPhoto
     * @param firstName
     * @param lastName
     * @param gender
     * @param dateOfBirth
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static usersAdminNewUser(
        username: string,
        password: string,
        email: string,
        mobile?: string,
        userPhoto?: string,
        firstName?: string,
        lastName?: string,
        gender?: string,
        dateOfBirth?: string,
    ): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users_admin/new_user',
            query: {
                'username': username,
                'password': password,
                'email': email,
                'mobile': mobile,
                'user_photo': userPhoto,
                'first_name': firstName,
                'last_name': lastName,
                'gender': gender,
                'date_of_birth': dateOfBirth,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User Pofile
     * @param requestBody
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static usersAdminUpdateUserPofile(
        requestBody: UserUpdate,
    ): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users_admin/user_update',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Email Validation By Username
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminGetEmailValidationByUsername(
        username: string,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users_admin/get_email_validation/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Validate User Email
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminValidateUserEmail(
        username: string,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users_admin/validate_email/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Disable User Profile
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminDisableUserProfile(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users_admin/disable_user/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Enable User Profile
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminEnableUserProfile(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users_admin/enable_user/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Validate User Mobile
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminValidateUserMobile(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/users_admin/validate_mobile/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Is User Player
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminIsUserPlayer(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users_admin/user_is_player/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Is User Manager
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminIsUserManager(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users_admin/user_is_manager/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Is User Coach
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminIsUserCoach(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users_admin/user_is_coach/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Is User Referee
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminIsUserReferee(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users_admin/user_is_referee/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete User Profile
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static usersAdminDeleteUserProfile(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/users_admin/delete_user/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a User Administrator`,
                422: `Validation Error`,
            },
        });
    }

}
