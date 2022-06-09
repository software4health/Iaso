import { getRequest } from '../../../../../hat/assets/js/apps/Iaso/libs/Api';
import { useSnackQuery } from '../../../../../hat/assets/js/apps/Iaso/libs/apiHooks';

export const useGetCampaignScope = ({ country, campaignId }) => {
    return useSnackQuery(
        ['polio', 'campaigns', country, campaignId],
        () => getRequest(`/api/polio/campaigns/?country__id__in=${country}`),
        undefined,
        {
            select: data => {
                const selectedCampaign = data?.find(
                    campaign => campaign.id === campaignId,
                );
                return selectedCampaign?.group?.org_units ?? [];
            },
        },
    );
};