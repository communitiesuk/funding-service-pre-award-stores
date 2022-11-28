from jsonschema import validate
from config.mappings.assessment_mapping_schema import top_level_assessment_mapping_schema as schema
from config import Config


def test_assessment_mapping_conforms_to_schema():
    assert validate(instance=Config.COF_R2W2_ASSESSMENT_MAPPING, schema=schema) == None
