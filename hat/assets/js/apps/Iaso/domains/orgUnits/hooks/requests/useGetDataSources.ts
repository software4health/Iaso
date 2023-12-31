/* eslint-disable camelcase */
import { UseQueryResult } from 'react-query';

import { getRequest } from '../../../../libs/Api';
import { useSnackQuery } from '../../../../libs/apiHooks';

import { DropdownOptions } from '../../../../types/utils';

import { DataSourcesApi } from '../../types/dataSources';

import { staleTime } from '../../config';

const getDataSources = (): Promise<DataSourcesApi> => {
    return getRequest('/api/datasources/');
};

export const useGetDataSources = (): UseQueryResult<
    DropdownOptions<string>[],
    Error
> => {
    const queryKey: any[] = ['sources'];
    // @ts-ignore
    return useSnackQuery({
        queryKey,
        queryFn: () => getDataSources(),
        options: {
            staleTime,
            select: data => {
                if (!data) return [];
                return data.sources.map(dataSource => {
                    return {
                        value: dataSource.id.toString(),
                        label: dataSource.name,
                        original: dataSource,
                    };
                });
            },
        },
    });
};
