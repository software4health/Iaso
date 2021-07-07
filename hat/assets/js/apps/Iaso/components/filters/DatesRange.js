import React from 'react';
import moment from 'moment';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import { KeyboardDatePicker } from '@material-ui/pickers';
import { FormControl, Grid, Tooltip, IconButton } from '@material-ui/core';
import Clear from '@material-ui/icons/Clear';
import { injectIntl } from 'bluesquare-components';
import MESSAGES from './messages';

const useStyles = makeStyles(theme => ({
    formControl: {
        width: '100%',
        marginBottom: theme.spacing(),
        marginTop: theme.spacing(),
    },
    clearDateButton: {
        marginRight: theme.spacing(2),
        padding: 0,
        position: 'absolute',
        right: theme.spacing(6),
        top: 15,
    },
}));

const DatesRange = ({
    dateFrom,
    dateTo,
    onChangeDate,
    intl: { formatMessage },
    displayedDateFormat,
}) => {
    const classes = useStyles();
    // Converting the displayedDateFormat to this one onChange to avoid a nasty bug in Firefox
    const dateFormat = 'DD-MM-YYYY';
    return (
        <Grid container spacing={4}>
            <Grid item xs={6}>
                <FormControl className={classes.formControl}>
                    <KeyboardDatePicker
                        autoOk
                        disableToolbar
                        variant="inline"
                        maxDate={
                            dateTo === '' || dateTo === null
                                ? undefined
                                : moment(dateTo, displayedDateFormat)
                        }
                        InputLabelProps={{
                            shrink: Boolean(dateFrom),
                        }}
                        format={displayedDateFormat}
                        label={formatMessage(MESSAGES.from)}
                        helperText=""
                        inputVariant="outlined"
                        value={
                            dateFrom === '' || dateFrom === null
                                ? null
                                : moment(dateFrom, displayedDateFormat)
                        }
                        onChange={date =>
                            onChangeDate(
                                'dateFrom',
                                date ? date.format(dateFormat) : null,
                            )
                        }
                    />
                    {dateFrom && (
                        <Tooltip arrow title={formatMessage(MESSAGES.clear)}>
                            <IconButton
                                color="inherit"
                                onClick={() => onChangeDate('dateFrom', null)}
                                className={classes.clearDateButton}
                            >
                                <Clear color="primary" />
                            </IconButton>
                        </Tooltip>
                    )}
                </FormControl>
            </Grid>
            <Grid item xs={6}>
                <FormControl className={classes.formControl}>
                    <KeyboardDatePicker
                        autoOk
                        disableToolbar
                        inputVariant="outlined"
                        variant="inline"
                        minDate={
                            dateFrom === '' || dateFrom === null
                                ? undefined
                                : moment(dateFrom, displayedDateFormat)
                        }
                        InputLabelProps={{
                            shrink: Boolean(dateTo),
                        }}
                        format={displayedDateFormat}
                        label={formatMessage(MESSAGES.to)}
                        helperText=""
                        value={
                            dateTo === '' || dateTo === null
                                ? null
                                : moment(dateTo, displayedDateFormat)
                        }
                        onChange={date =>
                            onChangeDate(
                                'dateTo',
                                date ? date.format(dateFormat) : null,
                            )
                        }
                    />
                    {dateTo && (
                        <Tooltip arrow title={formatMessage(MESSAGES.clear)}>
                            <IconButton
                                color="inherit"
                                onClick={() => onChangeDate('dateTo', null)}
                                className={classes.clearDateButton}
                            >
                                <Clear color="primary" />
                            </IconButton>
                        </Tooltip>
                    )}
                </FormControl>
            </Grid>
        </Grid>
    );
};

DatesRange.defaultProps = {
    dateFrom: '',
    dateTo: '',
    displayedDateFormat: 'DD/MM/YYYY',
    onChangeDate: () => null,
};

DatesRange.propTypes = {
    onChangeDate: PropTypes.func,
    dateFrom: PropTypes.string,
    dateTo: PropTypes.string,
    displayedDateFormat: PropTypes.string,
    intl: PropTypes.object.isRequired,
};

const DatesRangeIntl = injectIntl(DatesRange);

export default DatesRangeIntl;
