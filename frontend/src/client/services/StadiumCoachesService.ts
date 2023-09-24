/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StadiumCoachLink } from '../models/StadiumCoachLink';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StadiumCoachesService {

    /**
     * Read Coach Stadiums
     * @param coachUsername
     * @returns StadiumCoachLink Successful Response
     * @throws ApiError
     */
    public static stadiumCoachesReadCoachStadiums(
        coachUsername: string,
    ): CancelablePromise<Array<StadiumCoachLink>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadium_coaches/get_coach_stadiums/{coach_username}',
            path: {
                'coach_username': coachUsername,
            },
            errors: {
                404: `Stadium Coaches Not found`,
                422: `Validation Error`,
            },
        });
    }

}
