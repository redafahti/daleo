/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StadiumRefereeLink } from '../models/StadiumRefereeLink';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class StadiumRefereesService {

    /**
     * Read Referee Stadiums
     * @param refereeUsername
     * @returns StadiumRefereeLink Successful Response
     * @throws ApiError
     */
    public static stadiumRefereesReadRefereeStadiums(
        refereeUsername: string,
    ): CancelablePromise<Array<StadiumRefereeLink>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stadium_referees/get_referee_stadiums/{referee_username}',
            path: {
                'referee_username': refereeUsername,
            },
            errors: {
                404: `Stadium referees Not found`,
                422: `Validation Error`,
            },
        });
    }

}
