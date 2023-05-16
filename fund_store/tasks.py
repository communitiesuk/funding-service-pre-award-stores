from colored import attr
from colored import fg
from colored import stylize
from invoke import task

ECHO_STYLE = fg("light_gray") + attr("bold")


@task
def recreate_local_db(c, database_host="localhost", db_name="fsd_fund_store_1"):
    """Create a clean database for testing"""
    c.run(f"dropdb -h {database_host} --if-exists {db_name} --force")
    print(
        stylize(
            f"{db_name} db dropped from {database_host}...",
            ECHO_STYLE,
        )
    )
    c.run(f"createdb -h {database_host} {db_name}")
    c.run(
        f'psql -h {database_host} -d {db_name} -c "create extension if not'
        ' exists ltree;"'
    )
    print(stylize(f"{db_name} db created on {database_host}...", ECHO_STYLE))


@task
def init_migr(c, database_host="localhost", db_name="fsd_fund_store_1"):
    c.run("rm -rf ./db/migrations/")
    print(stylize("Deleted migrations", ECHO_STYLE))
    c.run("flask db init")
    print(
        stylize(
            "Run db init",
            ECHO_STYLE,
        )
    )
    c.run("flask db migrate -m 'Initial migration'")
    print(
        stylize(
            "Run migrate",
            ECHO_STYLE,
        )
    )


@task
def seed_db(c, database_host="localhost", db_name="fsd_fund_store_1"):
    c.run("flask db upgrade")
    print(
        stylize(
            "Run upgrade",
            ECHO_STYLE,
        )
    )
    c.run(f"psql -h {database_host} -d {db_name} -a -f db/cof_sql/fund.sql")
    c.run(f"psql -h {database_host} -d {db_name} -a -f db/cof_sql/rounds.sql")
    c.run(f"psql -h {database_host} -d {db_name} -a -f db/cof_sql/sections.sql")
    c.run(
        f"psql -h {database_host} -d {db_name} -a -f db/cof_sql/assessment_fields.sql"
    )
    c.run(f"psql -h {database_host} -d {db_name} -a -f db/cof_sql/section_fields.sql")
    # c.run(
    #     f"psql -h {database_host} -d {db_name} -a -f"
    #     " db/cof_sql/translations.sql"
    # )
    c.run(f"psql -h {database_host} -d {db_name} -a -f db/cof_sql/form_name.sql")
    c.run(
        f'psql -h {database_host} -d {db_name} -c "select f.short_name as'
        " Fund, r.short_name as Round from round r join fund f on r.fund_id ="
        ' f.id";'
    )
    c.run(
        f'psql -h {database_host} -d {db_name} -c "select f.short_name,'
        " r.short_name, s.title, s.weighting, s.path from section s join"
        " round r on round_id=r.id join fund f on r.fund_id = f.id order by"
        ' path;"'
    )

    c.run(
        f'psql -h {database_host} -d {db_name} -c "select s.title, f.title'
        " from section s left outer join section_field sf on s.id ="
        " sf.section_id left outer join assessment_field f on sf.field_id ="
        ' f.id order by s.path, sf.display_order;"'
    )


def print_section(section, indent):
    indent += "  "
    print(f"{indent}{section.title}")
    for f in section.fields:
        print(f"{indent}  Q: {f.field.title}")
    for s in section.children:
        print_section(s, indent)


@task
def print_application_sections(c):
    from fsd_test_utils.test_config.useful_config import UsefulConfig
    from app import create_app
    from db.queries import get_application_sections_for_round

    target_round = UsefulConfig.COF_ROUND_2_ID
    target_fund = UsefulConfig.COF_FUND_ID

    app = create_app()
    with app.app_context():
        sections = get_application_sections_for_round(target_fund, target_round)
        for section in sections:
            print_section(section, "")


@task
def print_assessment_sections(c):
    from fsd_test_utils.test_config.useful_config import UsefulConfig
    from app import create_app
    from db.queries import get_assessment_sections_for_round

    target_round = UsefulConfig.COF_ROUND_2_ID
    target_fund = UsefulConfig.COF_FUND_ID

    app = create_app()
    with app.app_context():
        sections = get_assessment_sections_for_round(target_fund, target_round)
        for section in sections:
            print_section(section, "")
