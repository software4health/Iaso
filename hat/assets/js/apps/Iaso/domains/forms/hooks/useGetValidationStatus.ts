import { UseQueryResult } from 'react-query';
import { defineMessages } from 'react-intl';

import { useSafeIntl, Pagination } from 'bluesquare-components';
import { useSnackQuery } from '../../../libs/apiHooks';
import { getRequest } from '../../../libs/Api';
import { DropdownOptions } from '../../../types/utils';

const MESSAGES = defineMessages({
    all: {
        id: 'iaso.forms.all',
        defaultMessage: 'All',
    },
    REJECTED: {
        defaultMessage: 'Rejected',
        id: 'iaso.forms.rejected',
    },
    NEW: {
        defaultMessage: 'New',
        id: 'iaso.forms.new',
    },
    VALID: {
        defaultMessage: 'Validated',
        id: 'iaso.forms.validated',
    },
    CLOSED: {
        defaultMessage: 'Closed',
        id: 'iaso.forms.closed',
    },
});

type Status = [string, string];

export interface ValidationStatusApiResult extends Pagination {
    results: Status[];
}

export const useGetValidationStatus = (
    includeAll = false,
): UseQueryResult<DropdownOptions<string>[], Error> => {
    const queryKey: any[] = ['validationStatus'];
    const { formatMessage } = useSafeIntl();
    return useSnackQuery({
        queryKey,
        queryFn: () => getRequest('/api/validationstatus/'),
        options: {
            retry: false,
            keepPreviousData: true,
            select: (data: ValidationStatusApiResult) => {
                const options: DropdownOptions<string>[] = data.results.map(
                    (status: Status) => ({
                        value: status[0],
                        label: MESSAGES[status[0]]
                            ? formatMessage(MESSAGES[status[0]])
                            : status[0],
                    }),
                );
                if (includeAll) {
                    options.unshift({
                        value: 'all',
                        label: formatMessage(MESSAGES.all),
                    });
                }
                return options;
            },
        },
    });
};
