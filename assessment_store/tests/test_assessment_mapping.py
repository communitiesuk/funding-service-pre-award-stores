from config import Config
from config.mappings.assessment_mapping_schema import (
    top_level_assessment_mapping_schema as schema,
)
from jsonschema import validate


def test_assessment_mapping_conforms_to_schema():
    assert (
        validate(instance=Config.COF_R2W2_ASSESSMENT_MAPPING, schema=schema)
        is None
    )
