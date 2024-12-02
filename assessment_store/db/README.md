# The Database Module 🗃

This module contains all code relating to database operations, including the querying of data.

- **migrations** contains the alembic generated migrations. Edit these manually at your own peril.
- **models** contains the ORM schemas defining a table in the database, along with associated objects such as ENUMS. The intended import path for these is `from db.models.{TABLE} import {TABLE}`.
- **queries** contains the operations we perform on the database ("queries"). These are not defined in the table objects because of possible circular imports and lack of separation of concerns. The intended import path for these is `from db.queries.{TABLE} import {QUERY NAME}`, or `from db.queries import {QUERY NAME}` for queries which involve multiple tables (although shouldn't you be using a foreign key in a specific table for this though 🤨).
- **schemas** contains all the marshmallow classes used for serialization. Intended import path is  `from db.schemas import {CLASS NAME}`.
