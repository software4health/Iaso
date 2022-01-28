/* eslint-disable react/require-default-props */
import React, {
    FunctionComponent,
    useState,
    useCallback,
    useMemo,
} from 'react';
import { Box, Paper } from '@material-ui/core';
import { useSafeIntl, Table } from 'bluesquare-components';
import MESSAGES from '../../constants/messages';
import {
    LqasImCampaignDataWithNameAndRegion,
    RoundString,
} from '../../constants/types';
import { makeDataForTable } from '../../pages/LQAS/utils';
import {
    sortbyDistrictNameAsc,
    sortbyDistrictNameDesc,
    sortbyRegionNameAsc,
    sortbyRegionNameDesc,
} from './tableUtils';
import { useConvertedLqasImData } from '../../pages/IM/requests';
import { CaregiversTableHeader } from './CaregiversTableHeader';
import { floatToPercentString } from '../../utils';
import { CaregiverInfoSource } from './CaregiverInfoSource';

type Props = {
    marginTop?: boolean;
    campaign?: string;
    round: RoundString;
    country?: number;
};

type SortValues = 'district_name' | 'region_name';

const columns = formatMessage => [
    {
        Header: formatMessage(MESSAGES.region),
        id: 'region_name',
        accessor: 'region_name',
    },
    {
        Header: formatMessage(MESSAGES.district),
        id: 'district_name',
        accessor: 'name',
    },
    {
        Header: formatMessage(MESSAGES.caregivers_informed),
        id: 'caregivers_informed',
        accessor: 'caregivers_informed',
        sortable: false,
        Cell: settings =>
            floatToPercentString(
                settings.row.original.care_giver_stats
                    .caregivers_informed_ratio,
            ),
    },
    {
        Header: formatMessage(MESSAGES.mainCaregiverInfoSource),
        id: 'mainCaregiverInfoSource',
        accessor: 'mainCaregiverInfoSource',
        sortable: false,
        Cell: settings => (
            <CaregiverInfoSource district={settings.row.original} />
        ),
    },
];
const defaultSorted = [{ id: 'region_name', desc: false }];

export const CaregiversTable: FunctionComponent<Props> = ({
    marginTop = true,
    campaign = '',
    round,
    country,
}) => {
    const { formatMessage } = useSafeIntl();
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [sortBy, setSortBy] = useState('asc');
    const [sortFocus, setSortFocus] = useState<SortValues>('region_name');
    const [resetPageToOne, setResetPageToOne] = useState(`${rowsPerPage}`);

    const { data: lqasImData, isLoading } = useConvertedLqasImData(
        'lqas',
        country,
    );
    const data = useMemo((): LqasImCampaignDataWithNameAndRegion[] => {
        return makeDataForTable(lqasImData, campaign, round);
    }, [lqasImData, campaign, round]);

    const handleSort = useCallback(
        focus => {
            if (sortFocus !== focus) {
                setSortFocus(focus);
                setSortBy('asc');
            } else if (sortBy === 'asc') {
                setSortBy('desc');
            } else {
                setSortBy('asc');
            }
        },
        [sortBy, sortFocus],
    );

    const handleTableParamsChange = params => {
        if (params.order) {
            handleSort(params.order.replace('-', ''));
        }
        if (params.pageSize) {
            setResetPageToOne(`${params.pageSize}`);
            setRowsPerPage(parseInt(params.pageSize, 10));
        }
        if (params.page) {
            setPage(parseInt(params.page, 10) - 1);
        }
    };

    const formatDataForTable = useCallback(
        (
            tableData: LqasImCampaignDataWithNameAndRegion[],
            // eslint-disable-next-line no-unused-vars
            sortFunc: (a: any, b: any) => number,
        ) =>
            tableData
                .sort(sortFunc)
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
        [page, rowsPerPage],
    );

    const dataForTable = useMemo(() => {
        if (sortFocus === 'district_name' && sortBy === 'asc') {
            return formatDataForTable(data, sortbyDistrictNameAsc);
        }
        if (sortFocus === 'district_name' && sortBy === 'desc') {
            return formatDataForTable(data, sortbyDistrictNameDesc);
        }
        if (sortFocus === 'region_name' && sortBy === 'asc') {
            return formatDataForTable(data, sortbyRegionNameAsc);
        }
        if (sortFocus === 'region_name' && sortBy === 'desc') {
            return formatDataForTable(data, sortbyRegionNameDesc);
        }
        console.warn(
            `Sort error, there must be a wrong parameter. Received: ${sortBy}, ${sortFocus}. Expected a combination of asc|desc and district_name|region_name`,
        );
        return [];
    }, [sortBy, sortFocus, data, formatDataForTable]);

    const pages = useMemo(
        () => (data?.length ? Math.ceil(data?.length / rowsPerPage) : 0),
        [data, rowsPerPage],
    );
    const params = useMemo(
        () => ({
            pageSize: rowsPerPage,
            page,
        }),
        [rowsPerPage, page],
    );

    return (
        <>
            {!isLoading && campaign && (
                <>
                    <CaregiversTableHeader
                        campaign={campaign}
                        round={round}
                        country={country}
                    />
                    <Box mt={marginTop ? 4 : 0} mb={4}>
                        <Paper elevation={3}>
                            <Table
                                countOnTop={false}
                                data={dataForTable}
                                pages={pages}
                                defaultSorted={defaultSorted}
                                columns={columns(formatMessage)}
                                marginTop={false}
                                count={data?.length ?? 0}
                                params={params}
                                resetPageToOne={resetPageToOne}
                                onTableParamsChange={handleTableParamsChange}
                            />
                        </Paper>
                    </Box>
                </>
            )}
        </>
    );
};
