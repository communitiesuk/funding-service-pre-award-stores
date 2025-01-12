from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovCheckboxesInput, GovSubmitInput
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

from proto.common.data.models import TemplateSection


class ChooseTemplateSectionsForm(FlaskForm):
    sections = SelectMultipleField(
        "Choose templates from the question bank",
        widget=GovCheckboxesInput(),
        validators=[DataRequired("Select at least one section")],
    )
    submit = SubmitField("Continue", widget=GovSubmitInput())

    def __init__(self, template_sections: list[TemplateSection], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_sections = template_sections

        self.sections.choices = [(section.id, section.title) for section in self.template_sections]

    @property
    def section_questions(self):
        return [
            [question.title for question in template_section.template_questions]
            for template_section in self.template_sections
        ]
