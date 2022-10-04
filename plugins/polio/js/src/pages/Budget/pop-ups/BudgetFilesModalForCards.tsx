import React, { FunctionComponent, useCallback } from 'react';
import {
    Box,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    Typography,
} from '@material-ui/core';
// @ts-ignore
import { useSafeIntl } from 'bluesquare-components';
import moment from 'moment';
import MESSAGES from '../../../constants/messages';
import { makeFileLinks, makeLinks } from '../utils';
import {
    Nullable,
    Optional,
} from '../../../../../../../hat/assets/js/apps/Iaso/types/utils';

type Props = {
    open: boolean;
    setOpen: React.Dispatch<React.SetStateAction<boolean>>;
    // eslint-disable-next-line react/require-default-props
    note?: Nullable<string>;
    date: string;
    links: Optional<Nullable<string[]>>;
    files: string[];
    author: string;
    type?: string;
};

export const BudgetFilesModalForCards: FunctionComponent<Props> = ({
    open,
    setOpen,
    note,
    date,
    links,
    author,
    type = '',
    files,
}) => {
    const { formatMessage } = useSafeIntl();

    const handleClose = useCallback(() => {
        setOpen(false);
    }, [setOpen]);
    return (
        <>
            <Dialog
                open={open}
                onClose={handleClose}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                    {formatMessage(MESSAGES.budgetFiles, {
                        type,
                        date: moment(date).format('L'),
                        author,
                        recipients: [],
                    })}
                </DialogTitle>
                <DialogContent>
                    <Divider />

                    <Box mt={2}>
                        {makeFileLinks(files)}
                        {makeLinks(links)}
                        {note && (
                            <>
                                {(files?.length > 0 ||
                                    (links?.length ?? []) > 0) && (
                                    <Box mt={4}>
                                        <Divider />
                                    </Box>
                                )}
                                <Box mb={2} mt={2}>
                                    <Typography style={{ fontWeight: 'bold' }}>
                                        {formatMessage(MESSAGES.notes)}
                                    </Typography>
                                </Box>
                                <Typography
                                    variant="body2"
                                    style={{
                                        whiteSpace: 'pre-line',
                                        // @ts-ignore
                                        wordWrap: 'anywhere',
                                    }}
                                >
                                    {note}
                                </Typography>
                            </>
                        )}
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
                        {formatMessage(MESSAGES.close)}
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
};
