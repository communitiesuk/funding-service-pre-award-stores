import json
import os
import sys

import click

sys.path.insert(1, ".")

from airium import Airium  # noqa: E402

from app import create_app  # noqa: E402
from fund_store.db.models.section import Section  # noqa: E402
from fund_store.db.queries import (
    get_application_sections_for_round,  # noqa: E402
    get_round_by_short_name,  # noqa: E402
)
from fund_store.scripts.all_questions.metadata_utils import (  # noqa: E402
    generate_print_data_for_sections,
)
from fund_store.scripts.all_questions.read_forms import (  # noqa: E402; , build_form  # noqa: E402
    find_forms_dir,
)

# Initialise Airium html printer
air = Airium()

# Define start and end html
BOILERPLATE_START = """
{% extends "base.html" %}
{%- from 'govuk_frontend_jinja/components/inset-text/macro.html' import govukInsetText -%}
{%- from "govuk_frontend_jinja/components/button/macro.html" import govukButton -%}

{% from "partials/file-formats.html" import file_formats %}
{% set pageHeading %}{% trans %}Full list of application questions{% endtrans %}{% endset %}
{% block content %}
<div class="govuk-grid-row">
    <div class="govuk-grid-column-two-thirds">
        <span class="govuk-caption-l">{% trans %}{{fund_title}}{% endtrans %} {% trans %}{{round_title}}{% endtrans %}
        </span>
        <h1 class="govuk-heading-xl">{{pageHeading}}</h1>
"""

BOILERPLATE_END = """
    </div>
</div>
{% endblock %}
"""


def print_html_toc(air: Airium, sections: dict):
    """Prints a table of contents for the supplied sections to the supplied `Airium` instance

    Args:
        air (Airium): Instance to write html to
        sections (dict): Sections for this TOC
    """
    with air.h2(klass="govuk-heading-m "):
        air("{% trans %}Table of contents{% endtrans %}")
    with air.ol(klass="govuk-list govuk-list--number"):
        for anchor, details in sections.items():
            with air.li():
                with air.a(klass="govuk-link", href=f"#{anchor}"):
                    air(details["title_text"])


def print_components(air: Airium, components: list):
    """Prints the components within a page

    Args:
        air (Airium): Instance to print html
        components (list): List of components to print
    """
    for c in components:
        # Print the title
        if not c["hide_title"] and c["title"] is not None:
            with air.p(klass="govuk-body"):
                air(f"{c['title']}")

        for t in c["text"]:
            # Print lists as <ul> bullet lists
            if isinstance(t, list):
                with air.ul(klass="govuk-list govuk-list--bullet"):
                    for bullet in t:
                        with air.li(klass=""):
                            air(bullet)
            else:
                # Just print the text
                with air.p(klass="govuk-body"):
                    air(t)


def print_html(sections: dict) -> str:
    """Prints the html for the supplied sections

    Args:
        sections (dict): All sections to print, as generated by `metadata_utils.generate_print_data_for_sections`

    Returns:
        str: HTML string
    """
    with air.div(klass="govuk-!-margin-bottom-8"):
        # Print Table of Contents
        print_html_toc(air, sections)
        idx_section = 1

        for anchor, details in sections.items():
            if anchor == "assessment_display_info":
                continue
            air.hr(klass="govuk-section-break govuk-section-break--l govuk-section-break--visible")

            # Print each section header, with anchor
            with air.h2(klass="govuk-heading-l", id=anchor):
                air(f"{idx_section}. {details['title_text']}")

            form_print_data = details["form_print_data"]
            # Sort in order of numbered headings
            for heading in sorted(
                form_print_data,
                key=lambda item: str((form_print_data[item])["heading_number"]),
            ):
                header_info = form_print_data[heading]
                # Print header for this form
                if header_info["is_form_heading"]:
                    with air.h3(klass="govuk-heading-m"):
                        air(f"{header_info['heading_number']}. {header_info['title']}")

                else:
                    # Print header for this form page
                    with air.h4(klass="govuk-heading-s"):
                        air(f"{header_info['heading_number']}. {header_info['title']}")

                # Print components within this form
                print_components(air, header_info["components"])

            idx_section += 1

    # Concatenate start html, generated html and end html to one string and return
    html = f"{BOILERPLATE_START}{str(air)}{BOILERPLATE_END}"
    print(html)
    return html


@click.command()
@click.option("--fund_short_code", default="cyp", help="Fund short code", prompt=True)
@click.option("--round_short_code", default="R1", help="Round short code", prompt=True)
@click.option(
    "--lang",
    default="en",
    help="Language - used when a round supports english and welsh",
    prompt=True,
    type=click.Choice(["en", "cy"]),
)
@click.option(
    "--output_location",
    default="../funding-service-design-frontend/app/templates/all_questions/",
    help="Folder to write output html to (language code will be appended as an intermediate path)",
    prompt=True,
)
@click.option(
    "--forms_dir",
    default="../digital-form-builder/fsd_config/form_jsons/",
    help="Local, absolute path, to the form JSONs to use to generate question lists",
    prompt=True,
)
@click.option(
    "--include_assessment_display_info",
    default=True,
    help="Whether to output the assessment display field info",
    prompt=True,
)
@click.option(
    "--assessment_display_output_path",
    default=".",
    help="Where to store assessment field display info",
    prompt=True,
)
def generate_all_questions(
    fund_short_code: str = None,
    round_short_code: str = None,
    lang: str = None,
    output_location: str = None,
    forms_dir: str = None,
    include_assessment_display_info: bool = False,
    assessment_display_output_path: str = None,
):
    app = create_app()
    with app.app.app_context():
        round = get_round_by_short_name(fund_short_code, round_short_code)
        if not round:
            raise NameError(f"Round {round_short_code} does not exist in fund {fund_short_code}")
        sections: list[Section] = get_application_sections_for_round(round.fund_id, round.id)

        path_to_form_jsons = find_forms_dir(forms_dir, fund_short_code, round_short_code, lang)

        section_map = generate_print_data_for_sections(
            sections=sections,
            path_to_form_jsons=path_to_form_jsons,
            lang=lang,
            include_assessment_field_details=include_assessment_display_info,
        )
        if include_assessment_display_info:
            to_write = {}
            for _anchor, section in section_map.items():
                for form_name, fields in section["assessment_display_info"].items():
                    to_write[form_name] = fields
            with open(
                os.path.join(
                    assessment_display_output_path,
                    f"{fund_short_code.casefold()}_{round_short_code.casefold()}_field_info_{lang}.json",
                ),
                "w",
            ) as f:
                json.dump(to_write, f)

        html_str = print_html(
            sections=section_map,
        )
        filename = f"{fund_short_code.casefold()}_{round_short_code.casefold()}_all_questions_{lang}.html"
        out_path = os.path.join(output_location, lang, filename)
        with open(out_path, "w") as f:
            f.write(html_str)


if __name__ == "__main__":
    generate_all_questions()