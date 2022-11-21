# Migrations.

This folder contains all of the code related to performing database migrations.

## Quick migrate.

If you would like to create a migration or run the migrations against your DB do the following:

- Set the `DATABASE_URL` to your DB connection string.
- Ensure that you have installed all the needed dependancies.
- Run `invoke bootstrap-dev-db` (This will create a db and upgrade it.)

To create a migration do the above and run:

`flask db migrate`

## Remarks.

### Alembic-utils

There is a library called alembic_utils which allows for one to define postgres specific functions and triggers. We use this to gureentee that the "jsonb_blob" column is immutatable once it has been inserted.

You will need to comment out `register_entities` in `db/migrations/env.py` if you are making a table with triggers on it within the same migration. This will make just the table migrations. Uncomment it to then create another migration with the triggers. Annoying, alembic-utils cannot work out the dependancies of triggers.

### ENUMS and flask-migrate

The use of ENUMs is not supported by alembic, so the follow has to be manually added to the downgrade command in the migration which creates the ENUM.
```python
op.execute(
"""
DROP TYPE status;
"""
)
```
