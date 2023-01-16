from config.mappings.assessment_mapping import (
    cof_r2w2_assessment_mapping as cof_r2w2,
)
from fsd_utils import CommonConfig

fund_round_to_assessment_mapping = {
    f"{CommonConfig.COF_FUND_ID}:{CommonConfig.COF_ROUND_2_ID}": cof_r2w2,
}
