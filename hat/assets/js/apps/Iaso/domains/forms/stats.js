import React from 'react';
import { Box, Grid } from '@material-ui/core';
import { commonStyles, useSafeIntl } from 'bluesquare-components';
import { makeStyles } from '@material-ui/core/styles';
import TopBar from '../../components/nav/TopBarComponent';
import { InstancesPerFormGraph } from '../../components/instancesGraph';
import MESSAGES from './messages';

const useStyles = makeStyles(theme => ({
    ...commonStyles(theme),
    card: {
        border: 'gray solid',
        height: '500px',
        borderRadius: 5,
        padding: 10,
    },
}));

const FormsStats = () => {
    const classes = useStyles();
    const { formatMessage } = useSafeIntl();

    return (
        <>
            <TopBar title={formatMessage(MESSAGES.statsTitle)} />
            <Box className={classes.containerFullHeightNoTabPadded}>
                <Grid container>
                    <Grid xs={6} item className={classes.card}>
                        <InstancesPerFormGraph />
                    </Grid>
                </Grid>
            </Box>
        </>
    );
};
export default FormsStats;
