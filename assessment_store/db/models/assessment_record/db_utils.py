from alembic_utils.pg_extension import PGExtension
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

# A method of imposing a database level block to mutating application json.

block_json_func = PGFunction(
    schema="public",
    signature="block_blob_mutate()",
    definition="""RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
        IF NEW.jsonb_blob <> OLD.jsonb_blob THEN
        RAISE EXCEPTION 'Cannot mutate application json.';
        END IF;
        RETURN NEW;
    END;
    $$""",
)

block_json_updates_trig = PGTrigger(
    schema="public",
    signature="block_updates_on_app_blob",
    definition="""
    BEFORE UPDATE
    ON assessment_records
    FOR EACH ROW
    EXECUTE PROCEDURE block_blob_mutate();""",
    on_entity="assessment_records",
)

extension = PGExtension(
    schema="public",
    signature="pg_trgm",
)
