import React from 'react';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import { Tooltip } from '@material-ui/core';

// eslint-disable-next-line import/no-named-as-default
// eslint-disable-next-line import/no-named-as-default-member
import {
    IconButton as IconButtonComponent,
    textPlaceholder,
} from 'bluesquare-components';
import DataSourceDialogComponent from './components/DataSourceDialogComponent';
import MESSAGES from './messages';
import { AddTask } from './components/AddTaskComponent';
import { ImportGeoPkgDialog } from './components/ImportGeoPkgDialog';

const dataSourcesTableColumns = (
    formatMessage,
    setForceRefresh,
    defaultSourceVersion,
) => [
    {
        Header: formatMessage(MESSAGES.defaultSource),
        accessor: 'defaultSource',
        sortable: false,
        Cell: settings =>
            defaultSourceVersion &&
            defaultSourceVersion.source &&
            defaultSourceVersion.source.id === settings.cell.row.original.id && (
                <Tooltip title={formatMessage(MESSAGES.defaultSource)}>
                    <CheckCircleIcon color="primary" />
                </Tooltip>
            ),
    },
    {
        Header: formatMessage(MESSAGES.defaultVersion),
        accessor: 'default_version__number',
        Cell: settings => {
            if (!settings.cell.row.original.default_version) return textPlaceholder;
            return <span>{settings.cell.row.original.default_version.number}</span>;
        },
    },
    {
        Header: formatMessage(MESSAGES.dataSourceName),
        accessor: 'name',
        Cell: settings => {
            return <span>{settings.cell.row.original.name}</span>;
        },
    },
    {
        Header: formatMessage(MESSAGES.dataSourceDescription),
        accessor: 'description',
        Cell: settings => <span>{settings.cell.row.original.description}</span>,
    },
    {
        Header: formatMessage(MESSAGES.dataSourceReadOnly),
        accessor: 'read_only',
        Cell: settings => (
            <span>
                {settings.cell.row.original.read_only === true
                    ? formatMessage(MESSAGES.yes)
                    : formatMessage(MESSAGES.no)}
            </span>
        ),
    },
    {
        Header: formatMessage(MESSAGES.actions),
        resizable: false,
        sortable: false,
        Cell: settings => {
            const sortedVersions = settings.cell.row.original.versions.sort(
                (v1, v2) => v2.number - v1.number,
            );
            const latestVersion =
                sortedVersions.length > 0 ? sortedVersions[0].number : 0;
            const addTaskTitle = {
                ...MESSAGES.addTaskTitle,
                values: {
                    title: formatMessage(MESSAGES.importFromDhis2),
                    source: settings.cell.row.original.name,
                    version: latestVersion + 1,
                },
            };
            const defaultVersion =
                settings.cell.row.original.default_version?.number ?? null;
            return (
                <section>
                    <DataSourceDialogComponent
                        renderTrigger={({ openDialog }) => (
                            <IconButtonComponent
                                onClick={openDialog}
                                icon="edit"
                                tooltipMessage={MESSAGES.edit}
                            />
                        )}
                        initialData={{
                            ...settings.cell.row.original,
                            projects: settings.cell.row.original.projects.flat(),
                        }}
                        defaultSourceVersion={defaultSourceVersion}
                        titleMessage={MESSAGES.updateDataSource}
                        key={settings.cell.row.original.updated_at}
                        onSuccess={() => setForceRefresh(true)}
                        sourceCredentials={
                            settings.cell.row.original.credentials
                                ? settings.cell.row.original.credentials
                                : {}
                        }
                    />
                    <AddTask
                        renderTrigger={({ openDialog }) => (
                            <IconButtonComponent
                                onClick={openDialog}
                                icon="download"
                                tooltipMessage={MESSAGES.importFromDhis2}
                            />
                        )}
                        defaultSourceVersion={defaultSourceVersion}
                        titleMessage={addTaskTitle}
                        key={`${settings.cell.row.original.updated_at} ${settings.cell.row.original.id} addTask`}
                        sourceId={settings.cell.row.original.id}
                        sourceVersion={latestVersion + 1}
                        sourceCredentials={
                            settings.cell.row.original.credentials
                                ? settings.cell.row.original.credentials
                                : {}
                        }
                    />
                    <ImportGeoPkgDialog
                        renderTrigger={({ openDialog }) => (
                            <IconButtonComponent
                                onClick={openDialog}
                                icon="globe"
                                tooltipMessage={MESSAGES.importGeoPkg}
                            />
                        )}
                        titleMessage={MESSAGES.geoPkgTitle}
                        sourceId={settings.cell.row.original.id}
                        sourceName={settings.cell.row.original.name}
                        latestVersion={latestVersion}
                        defaultVersion={defaultVersion}
                        projects={settings.cell.row.original.projects.flat()}
                    />
                </section>
            );
        },
    },
];
export default dataSourcesTableColumns;
