from sqlalchemy import select

from db import db
from proto.common.data.models import ApplicationQuestion, ApplicationSection, TemplateQuestion, TemplateSection


def get_template_sections_and_questions():
    template_sections = (
        db.session.scalars(select(TemplateSection).join(TemplateQuestion).order_by(TemplateSection.order))
        .unique()
        .all()
    )
    return template_sections


def add_template_sections_to_round(round_id, template_section_ids):
    template_sections = (
        db.session.scalars(
            select(TemplateSection).join(TemplateQuestion).filter(TemplateSection.id.in_(template_section_ids))
        )
        .unique()
        .all()
    )

    print(template_sections)

    sections = []
    for template_section in template_sections:
        section = ApplicationSection(
            slug=template_section.slug, title=template_section.title, order=template_section.order, round_id=round_id
        )
        db.session.add(section)
        sections.append(section)

        for template_question in template_section.template_questions:
            question = ApplicationQuestion(
                slug=template_question.slug,
                type=template_question.type,
                title=template_question.title,
                hint=template_question.hint,
                order=template_question.order,
                data_source=template_question.data_source,
                data_standard_id=template_question.data_standard_id,
                section_id=section.id,
                template_question_id=template_question.id,
            )
            section.application_questions.append(question)

    db.session.commit()
