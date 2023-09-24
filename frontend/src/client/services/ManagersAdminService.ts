/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ManagerRead } from '../models/ManagerRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ManagersAdminService {

    /**
     * Get All Managers
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static managersAdminGetAllManagers(): CancelablePromise<Array<ManagerRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers_admin/get_managers',
            errors: {
                418: `I'm an Administrator`,
            },
        });
    }

    /**
     * Create New Manager
     * @param username
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static managersAdminCreateNewManager(
        username: string,
    ): CancelablePromise<ManagerRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/managers_admin/create_manager/{username}',
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
     * Get Manager Profile
     * @param username
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static managersAdminGetManagerProfile(
        username: string,
    ): CancelablePromise<ManagerRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/managers_admin/get_manager/{username}',
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
     * Update Manager Profile
     * @param managerUsername
     * @param seasonRate
     * @returns ManagerRead Successful Response
     * @throws ApiError
     */
    public static managersAdminUpdateManagerProfile(
        managerUsername: string,
        seasonRate?: number,
    ): CancelablePromise<ManagerRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/managers_admin/update_manager/{username}',
            query: {
                'manager_username': managerUsername,
                'season_rate': seasonRate,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Manager Profile
     * @param username
     * @returns any Successful Response
     * @throws ApiError
     */
    public static managersAdminDeleteManagerProfile(
        username: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/managers_admin/delete_manager/{username}',
            path: {
                'username': username,
            },
            errors: {
                418: `I'm an Administrator`,
                422: `Validation Error`,
            },
        });
    }

}
