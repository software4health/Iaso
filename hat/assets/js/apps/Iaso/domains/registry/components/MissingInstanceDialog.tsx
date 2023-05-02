import React, { FunctionComponent, useCallback } from 'react';
import { useDispatch } from 'react-redux';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    makeStyles,
    Button,
} from '@material-ui/core';
import {
    useSafeIntl,
    makeFullModal,
    commonStyles,
    Table,
    IconButton,
} from 'bluesquare-components';
import EnketoIcon from '../../instances/components/EnketoIcon';

import { OrgUnit } from '../../orgUnits/types/orgUnit';

import { useGetCreateInstance } from '../hooks/useGetCreateInstance';

import { MissingInstanceButton } from './MissingInstanceButton';

import { redirectToReplace } from '../../../routing/actions';
import { RegistryDetailParams } from '../types';
import { baseUrls } from '../../../constants/urls';
import MESSAGES from '../messages';

type Props = {
    missingOrgUnits: OrgUnit[];
    isOpen: boolean;
    closeDialog: () => void;
    params: RegistryDetailParams;
    formId?: string;
};
const useStyles = makeStyles(theme => ({
    ...commonStyles(theme),
    paper: {
        overflow: 'visible',
    },
    title: {
        paddingBottom: 0,
    },
    content: {
        padding: 0,
        '& .MuiTableContainer-root': {
            maxHeight: '60vh',
            overflow: 'auto',
            // @ts-ignore
            borderTop: `1px solid ${theme.palette.ligthGray.border}`,
            // @ts-ignore
            borderBottom: `1px solid ${theme.palette.ligthGray.border}`,
        },
        '& .MuiTableHead-root': {
            position: 'sticky',
            top: 0,
            zIndex: 10,
        },
        '& .pagination-count': {
            marginRight: theme.spacing(2),
        },
    },
    action: {
        paddingBottom: theme.spacing(2),
        paddingRight: theme.spacing(2),
    },
}));

const MissingInstanceDialog: FunctionComponent<Props> = ({
    missingOrgUnits,
    closeDialog,
    isOpen,
    params,
    formId,
}) => {
    const dispatch = useDispatch();
    const classes: Record<string, string> = useStyles();
    const { formatMessage } = useSafeIntl();
    const handleClose = useCallback(() => {
        const newParams = {
            ...params,
        };
        delete newParams.missingSubmissionVisible;
        dispatch(redirectToReplace(baseUrls.registryDetail, newParams));
        closeDialog();
    }, [closeDialog, dispatch, params]);
    const creteInstance = useGetCreateInstance(window.location.href, formId);
    return (
        <Dialog
            fullWidth
            maxWidth="xs"
            open={isOpen}
            classes={{
                paper: classes.paper,
            }}
            onClose={handleClose}
            scroll="body"
            id="missing-submbissions"
            data-test="missing-submbissions"
        >
            <DialogTitle className={classes.title}>
                {formatMessage(MESSAGES.missingSubmission)}
            </DialogTitle>
            <DialogContent className={classes.content}>
                <Table
                    marginTop={false}
                    marginBottom={false}
                    data={missingOrgUnits}
                    pages={0}
                    defaultSorted={[{ id: 'name', desc: true }]}
                    columns={[
                        {
                            Header: formatMessage(MESSAGES.name),
                            id: 'name',
                            accessor: 'name',
                            align: 'left',
                            sortable: false,
                        },
                        {
                            Header: formatMessage(MESSAGES.add),
                            id: 'action',
                            accessor: 'action',
                            sortable: false,
                            width: 50,
                            Cell: settings => {
                                return (
                                    <IconButton
                                        onClick={() =>
                                            creteInstance(
                                                settings.row.original.id,
                                            )
                                        }
                                        overrideIcon={EnketoIcon}
                                        tooltipMessage={MESSAGES.createOnEnketo}
                                        iconSize="small"
                                        size="small"
                                    />
                                );
                            },
                        },
                    ]}
                    count={missingOrgUnits.length}
                    params={params}
                    showPagination={false}
                    elevation={0}
                />
            </DialogContent>
            <DialogActions className={classes.action}>
                <Button
                    onClick={() => {
                        handleClose();
                    }}
                    color="primary"
                    data-test="close-button"
                >
                    {formatMessage(MESSAGES.close)}
                </Button>
            </DialogActions>
        </Dialog>
    );
};
const modalWithButton = makeFullModal(
    MissingInstanceDialog,
    MissingInstanceButton,
);

export { modalWithButton as MissingInstanceDialog };