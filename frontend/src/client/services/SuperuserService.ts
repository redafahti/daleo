/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SuperuserService {

    /**
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static superuserReadRoot(): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/superuser/',
            errors: {
                418: `I'm a Superuser`,
            },
        });
    }

    /**
     * Get Status
     * @returns any Successful Response
     * @throws ApiError
     */
    public static superuserGetStatus(): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/superuser/status',
            errors: {
                418: `I'm a Superuser`,
            },
        });
    }

    /**
     * Make Superuser
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static superuserMakeSuperuser(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/superuser/make_superuser/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a Superuser`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Make Admin
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static superuserMakeAdmin(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/superuser/make_admin/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a Superuser`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Superuser
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static superuserRemoveSuperuser(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/superuser/remove_superuser/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a Superuser`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Admin
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static superuserRemoveAdmin(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/superuser/remove_admin/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm a Superuser`,
                422: `Validation Error`,
            },
        });
    }

}
