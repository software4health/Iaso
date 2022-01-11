import MESSAGES from '../../constants/messages';
import {
    BarChartData,
    FormatForNFMArgs,
    NfmRoundString,
} from '../../constants/types';
import { IM_PASS, IM_FAIL, IM_WARNING, ImNfmKeys } from './constants';
import { makeLegendItem, sortByDictKey } from '../../utils';
import { OK_COLOR, WARNING_COLOR, FAIL_COLOR } from '../../styles/constants';

export const determineStatusForDistrict = district => {
    if (!district) return null;
    const ratio =
        (district.total_child_fmd / district.total_child_checked) * 100;
    if (ratio >= 95) return IM_PASS;
    if (ratio > 89 && ratio < 95) return IM_WARNING;
    return IM_FAIL;
};

export const getImStatsForRound = (imData, campaign, round) => {
    if (!imData[campaign]) return [[], [], []];
    const allStatuses = [...imData[campaign][round]].map(district => {
        return determineStatusForDistrict(district);
    });
    const passed = allStatuses.filter(status => status === IM_PASS);
    const disqualified = allStatuses.filter(status => status === IM_WARNING);
    const failed = allStatuses.filter(status => status === IM_FAIL);

    return [passed, failed, disqualified];
};

export const makeImMapLegendItems =
    formatMessage => (imData, campaign, round) => {
        const [passed, failed, disqualified] = getImStatsForRound(
            imData,
            campaign,
            round,
        );
        const passedLegendItem = makeLegendItem({
            color: OK_COLOR,
            value: passed?.length,
            message: formatMessage(MESSAGES['1imOK']),
        });
        const disqualifiedLegendItem = makeLegendItem({
            color: WARNING_COLOR,
            value: disqualified?.length,
            message: formatMessage(MESSAGES['2imWarning']),
        });
        const failedLegendItem = makeLegendItem({
            color: FAIL_COLOR,
            value: failed?.length,
            message: formatMessage(MESSAGES['3imFail']),
        });

        return [passedLegendItem, disqualifiedLegendItem, failedLegendItem];
    };

export const formatImDataForChart = ({ data, campaign, round, regions }) => {
    const dataForRound = data[campaign] ? [...data[campaign][round]] : [];
    return regions
        .map(region => {
            const regionData = dataForRound.filter(
                district => district.region_name === region.name,
            );
            const aggregatedData = regionData
                .map(district => ({
                    marked: district.total_child_fmd,
                    checked: district.total_child_checked,
                }))
                .reduce(
                    (total, current) => {
                        return {
                            marked: total.marked + current.marked,
                            checked: total.checked + current.checked,
                        };
                    },
                    { marked: 0, checked: 0 },
                );
            const { checked, marked } = aggregatedData;
            // forcing aggregatedData.checked to 1 to avoid dividing by 0
            const markedRatio = (marked / (checked || 1)) * 100;
            return {
                name: region.name,
                value: Number.isSafeInteger(markedRatio)
                    ? markedRatio
                    : markedRatio.toFixed(2),
                marked: aggregatedData.marked,
                checked: aggregatedData.checked,
            };
        })
        .sort((a, b) => a.value < b.value);
};

export const imTooltipFormatter = formatMessage => (_value, _name, props) => {
    // eslint-disable-next-line react/prop-types
    const ratio = `${props.payload.checked}/${props.payload.marked}`;
    return [ratio, formatMessage(MESSAGES.vaccinated)];
};

const sortImNfmKeys = sortByDictKey("value");

export const formatImDataForNFMChart = ({
    data,
    campaign,
    round,
    formatMessage,
}: FormatForNFMArgs): BarChartData[] => {
    if (!data || !campaign || !data[campaign]) return [] as BarChartData[];
    const roundString: string = NfmRoundString[round];
    const campaignData: Record<string, number> = data[campaign][roundString];
    const entries: [string, number][] = Object.entries(campaignData);
    const convertedEntries = entries.map(entry => {
        const [name, value] = entry;
        return { name: formatMessage(MESSAGES[name]), value, nfmKey: name };
    });
    if (convertedEntries.length === ImNfmKeys.length)
        return convertedEntries.sort(sortImNfmKeys);

    const dataKeys = Object.keys(campaignData);
    const missingEntries = ImNfmKeys.filter(
        nfmKey => !dataKeys.includes(nfmKey),
    ).map(nfmKey => ({
        name: formatMessage(MESSAGES[nfmKey]),
        value: 0,
        nfmKey,
    }));
    return [...convertedEntries, ...missingEntries].sort(sortImNfmKeys);
};