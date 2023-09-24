/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UserRead } from '../models/UserRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class EmailValidationService {

    /**
     * Generate New Email Validation
     * @param email
     * @returns any Successful Response
     * @throws ApiError
     */
    public static emailValidationGenerateNewEmailValidation(
        email: string,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/generate_new_email_validation/{email}',
            path: {
                'email': email,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Validate User Email
     * @param email
     * @param validationCode
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static emailValidationValidateUserEmail(
        email: string,
        validationCode: string,
    ): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/validate_email/{email}/{validation_code}',
            path: {
                'email': email,
                'validation_code': validationCode,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
