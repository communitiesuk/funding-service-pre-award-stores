<!-- TEMPLATE 

We bundle our changes into unreleased. When someone creates a tag, they move it into a proper version heading.

    --
## VERSION [year-month-day]

### Added

### Changed

### Removed

### Fixed

### Security
    --

    You can link to other releases using [link text](#v1.1.1-year-month-day)

    Types of changes:
    Added: for new features.
    Changed: for changes in existing functionality.
    Deprecated: for soon-to-be removed features.
    Removed: for now removed features.
    Fixed: for any bug fixes.
    Security: in case of vulnerabilities. 
-->

# Changelog

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

### Added
- CHANGELOG.md (so meta).
- assessment_records table, complete with JSONB blob.
- The `/application_overviews/{fund_id}/{round_id}` endpoint.
- test set up which inserts data into a database rather then mocking endpoints and using envs to decide program flow.
- application test data, this file contains 1500 rows of application json for testing.
- SQL information read out after pytest completes. Controllable with `pytest --statementdetails=True,False`.
- Random data generation for pytest, useful for stress testing. Controllable with `pytest --randomdata=True --apps-per-round=int --rounds-per-fund=int --number-of-funds=int`.
- Tests for db functions and routes.
- Several new invoke tasks. They are in `tasks`, and described in `tasks/TASKS.md`.
- a `pdoc` (a auto-documentation generator) workflow which is triggered on tags.

### Changed
- folder structure has been changed dramatically to encourage better separation of concerns and modularity. The `README.md` in each module roughly explains the intended import paths from a folder. Queries are no longer methods within the table model class. If a property of a table model is important enough to include within the class than please consider using [hybrid properties](https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html) so that our queries remain fast and don't execute python needlessly.

### Removed
- Sqlalchemy table models. These are in a branch for when we have a stable vision of the data model and we are ready to refactor them.
- Old test set up, since it was linked to the old data model implementation.

## v1.0.0 DATE

### Added

### Changed

### Removed

### Fixed

### Security