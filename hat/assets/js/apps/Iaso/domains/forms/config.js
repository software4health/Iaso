import React from 'react';
import { Grid } from '@material-ui/core';
import { Link } from 'react-router';

import { IconButton as IconButtonComponent } from 'bluesquare-components';
import FormVersionsDialog from './components/FormVersionsDialogComponent';
import { baseUrls } from '../../constants/urls';
import { userHasPermission } from '../users/utils';
import MESSAGES from './messages';
import DeleteDialog from '../../components/dialogs/DeleteDialogComponent';
import { DateTimeCell } from '../../components/Cells/DateTimeCell';
import { YesNoCell } from '../../components/Cells/YesNoCell';

export const formVersionsTableColumns = (
    formatMessage,
    setForceRefresh,
    formId,
    periodType,
) => [
    {
        Header: formatMessage(MESSAGES.version),
        accessor: 'version_id',
    },
    {
        Header: formatMessage(MESSAGES.startPeriod),
        accessor: 'start_period',
    },
    {
        Header: formatMessage(MESSAGES.endPeriod),
        accessor: 'end_period',
    },
    {
        Header: formatMessage(MESSAGES.actions),
        accessor: 'actions',
        sortable: false,
        Cell: settings => (
            <section>
                {settings.row.original.xls_file && (
                    <IconButtonComponent
                        onClick={() =>
                            window.open(
                                settings.row.original.xls_file,
                                '_blank',
                            )
                        }
                        icon="xls"
                        tooltipMessage={MESSAGES.xls_form_file}
                    />
                )}
                <FormVersionsDialog
                    renderTrigger={({ openDialog }) => (
                        <IconButtonComponent
                            onClick={openDialog}
                            icon="edit"
                            tooltipMessage={MESSAGES.edit}
                        />
                    )}
                    onConfirmed={() => setForceRefresh(true)}
                    formVersion={settings.row.original}
                    periodType={periodType}
                    formId={formId}
                    titleMessage={{
                        ...MESSAGES.updateFormVersion,
                        values: {
                            version_id: settings.row.original.version_id,
                        },
                    }}
                    key={settings.row.original.updated_at}
                />
            </section>
        ),
    },
];

const formsTableColumns = ({
    formatMessage,
    user,
    deleteForm = () => null,
    orgUnitId,
    restoreForm = () => null,
    showDeleted,
}) => {
    const cols = [
        {
            Header: formatMessage(MESSAGES.name),
            accessor: 'name',
            style: { justifyContent: 'left' },
        },
        {
            Header: formatMessage(MESSAGES.created_at),
            accessor: 'created_at',
            Cell: DateTimeCell,
        },
        {
            Header: formatMessage(MESSAGES.updated_at),
            accessor: 'updated_at',
            Cell: DateTimeCell,
        },
        {
            Header: formatMessage(MESSAGES.instance_updated_at),
            accessor: 'instance_updated_at',
            Cell: DateTimeCell,
        },
        {
            Header: formatMessage(MESSAGES.singlePerPeriod),
            accessor: 'single_per_period',
            Cell: YesNoCell,
        },
        {
            Header: formatMessage(MESSAGES.type),
            sortable: false,
            accessor: 'org_unit_types',
            Cell: settings =>
                settings.row.original.org_unit_types
                    .map(o => o.short_name)
                    .join(', '),
        },
        {
            Header: formatMessage(MESSAGES.records),
            accessor: 'instances_count',
        },
        {
            Header: formatMessage(MESSAGES.form_id),
            accessor: 'form_id',
            sortable: false,
            style: { justifyContent: 'left' },
        },
        {
            Header: formatMessage(MESSAGES.latest_version_files),
            accessor: 'latest_version_files',
            sortable: false,
            Cell: settings =>
                settings.row.original.latest_form_version !== null && (
                    <Grid container spacing={1} justifyContent="center">
                        <Grid item>
                            {
                                settings.row.original.latest_form_version
                                    .version_id
                            }
                        </Grid>
                        <Grid container spacing={1} justifyContent="center">
                            {settings.row.original.latest_form_version
                                .xls_file && (
                                <Grid item>
                                    <Link
                                        download
                                        href={
                                            settings.row.original
                                                .latest_form_version.xls_file
                                        }
                                    >
                                        XLS
                                    </Link>
                                </Grid>
                            )}
                            <Grid item>
                                <Link
                                    download
                                    href={
                                        settings.row.original
                                            .latest_form_version.file
                                    }
                                >
                                    XML
                                </Link>
                            </Grid>
                        </Grid>
                    </Grid>
                ),
        },
        {
            Header: formatMessage(MESSAGES.actions),
            resizable: false,
            sortable: false,
            width: 250,
            accessor: 'actions',
            Cell: settings => {
                let urlToInstances = `${baseUrls.instances}/formIds/${settings.row.original.id}`;
                if (orgUnitId) {
                    urlToInstances = `${urlToInstances}/levels/${orgUnitId}`;
                }
                urlToInstances = `${urlToInstances}/tab/list`;
                return (
                    <section>
                        {showDeleted && (
                            <IconButtonComponent
                                onClick={() =>
                                    restoreForm(settings.row.original.id)
                                }
                                icon="restore-from-trash"
                                tooltipMessage={MESSAGES.restoreFormTooltip}
                            />
                        )}
                        {!showDeleted && (
                            <>
                                {userHasPermission(
                                    'iaso_submissions',
                                    user,
                                ) && (
                                    <IconButtonComponent
                                        url={`${urlToInstances}`}
                                        icon="remove-red-eye"
                                        tooltipMessage={MESSAGES.viewInstances}
                                    />
                                )}
                                {userHasPermission('iaso_forms', user) && (
                                    <IconButtonComponent
                                        url={`${baseUrls.formDetail}/formId/${settings.row.original.id}`}
                                        icon="edit"
                                        tooltipMessage={MESSAGES.edit}
                                    />
                                )}
                                {userHasPermission('iaso_forms', user) && (
                                    <IconButtonComponent
                                        url={`/forms/mappings/formId/${settings.row.original.id}/order/form_version__form__name,form_version__version_id,mapping__mapping_type/pageSize/20/page/1`}
                                        icon="dhis"
                                        tooltipMessage={MESSAGES.dhis2Mappings}
                                    />
                                )}
                                {userHasPermission('iaso_forms', user) && (
                                    <DeleteDialog
                                        titleMessage={MESSAGES.deleteFormTitle}
                                        onConfirm={closeDialog =>
                                            deleteForm(
                                                settings.row.original.id,
                                            ).then(closeDialog)
                                        }
                                    />
                                )}
                            </>
                        )}
                    </section>
                );
            },
        },
    ];
    if (showDeleted) {
        cols.splice(1, 0, {
            Header: formatMessage(MESSAGES.deleted_at),
            accessor: 'deleted_at',
            Cell: DateTimeCell,
        });
    }
    return cols;
};

export default formsTableColumns;
