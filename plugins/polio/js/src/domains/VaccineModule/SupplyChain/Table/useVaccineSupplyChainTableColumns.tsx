import React, { useMemo } from 'react';
import {
    Column,
    IconButton,
    textPlaceholder,
    useSafeIntl,
} from 'bluesquare-components';
// import { VACCINE_SUPPLY_CHAIN } from '../../../../constants/routes';
import {
    DateCell,
    MultiDateCell,
    MultiDateTimeCellRfc,
} from '../../../../../../../../hat/assets/js/apps/Iaso/components/Cells/DateTimeCell';
import MESSAGES from '../messages';
import DeleteDialog from '../../../../../../../../hat/assets/js/apps/Iaso/components/dialogs/DeleteDialogComponent';
import { useDeleteVrf } from '../hooks/api';

// const baseUrl = VACCINE_SUPPLY_CHAIN;

export const useVaccineSupplyChainTableColumns = (): Column[] => {
    const { formatMessage } = useSafeIntl();
    const { mutateAsync: deleteVrf } = useDeleteVrf();
    return useMemo(() => {
        return [
            {
                Header: formatMessage(MESSAGES.country),
                accessor: 'country.name',
                id: 'country',
                sortable: true,
            },
            {
                Header: formatMessage(MESSAGES.vaccine),
                accessor: 'vaccine_type',
                id: 'vaccine_type',
                sortable: true,
            },
            {
                Header: formatMessage(MESSAGES.obrName),
                accessor: 'obr_name',
                sortable: true,
            },

            {
                Header: formatMessage(MESSAGES.poNumbers),
                accessor: 'po_numbers',
                Cell: settings => {
                    const poNumbers = settings.row.original?.po_numbers ?? '';
                    const poNumbersList = poNumbers.split(',');
                    return (
                        <>
                            {poNumbersList.map(poNumber => (
                                <div key={poNumber}>
                                    {poNumber ?? textPlaceholder}
                                </div>
                            ))}
                        </>
                    );
                },
            },
            {
                Header: formatMessage(MESSAGES.rounds),
                id: 'rounds',
                Cell: settings => {
                    const { rounds } = settings.row.original;
                    return <span>{rounds.map(r => r.number).join(', ')}</span>;
                },
            },
            {
                Header: formatMessage(MESSAGES.startDate),
                accessor: 'start_date',
                sortable: false,
                Cell: DateCell,
            },
            {
                Header: formatMessage(MESSAGES.endDate),
                accessor: 'end_date',
                sortable: false,
                Cell: DateCell,
            },
            {
                Header: formatMessage(MESSAGES.dosesShipped),
                accessor: 'doses_shipped',
            },
            {
                Header: formatMessage(MESSAGES.estimatedDateOfArrival),
                accessor: 'eta',
                Cell: MultiDateTimeCellRfc,
            },
            {
                Header: 'VAR',
                accessor: 'var',
                Cell: MultiDateCell,
            },
            {
                Header: formatMessage(MESSAGES.actions),
                accessor: 'account',
                sortable: false,
                Cell: settings => {
                    return (
                        <>
                            <IconButton
                                icon="edit"
                                tooltipMessage={MESSAGES.edit}
                                // disabled
                                onClick={() => null}
                            />
                            {/* TODO make better DeleteDialog */}
                            <DeleteDialog
                                titleMessage={MESSAGES.deleteVRF}
                                message={MESSAGES.deleteVRFWarning}
                                onConfirm={() =>
                                    deleteVrf(settings.row.original.id)
                                }
                            />
                        </>
                    );
                },
            },
        ];
    }, [deleteVrf, formatMessage]);
};
