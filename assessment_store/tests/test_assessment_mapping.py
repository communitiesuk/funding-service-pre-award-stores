from jsonschema import validate

from config import Config
from config.mappings.assessment_mapping_schema import (
    top_level_assessment_mapping_schema as schema,
)


def test_assessment_mapping_conforms_to_schema():
    for _key, value in Config.ASSESSMENT_MAPPING_CONFIG.items():
        assert validate(instance=value, schema=schema) is None
