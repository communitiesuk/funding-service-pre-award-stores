from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovCheckboxesInput, GovRadioInput, GovSubmitInput, GovTextInput
from wtforms.fields.choices import RadioField, SelectMultipleField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Optional

from proto.common.data.models import TemplateSection
from proto.common.data.models.fund import FundingType


class CreateGrantForm(FlaskForm):
    code = StringField("Grant code", widget=GovTextInput(), validators=[DataRequired(message="Enter a grant code")])

    name = StringField(
        "Grant name", widget=GovTextInput(), validators=[DataRequired(message="Enter a name for the grant")]
    )
    name_cy = StringField("Grant name (Welsh)", widget=GovTextInput(), validators=[Optional()])

    title = StringField(
        "Grant title", widget=GovTextInput(), validators=[DataRequired(message="Enter a title for the grant")]
    )
    title_cy = StringField("Grant title (Welsh)", widget=GovTextInput(), validators=[Optional()])

    description = StringField(
        "Grant description",
        widget=GovTextInput(),
        validators=[DataRequired(message="Enter a description for the grant")],
    )
    description_cy = StringField("Grant description (Welsh)", widget=GovTextInput(), validators=[Optional()])

    welsh_available = RadioField(
        "Welsh available?",
        widget=GovRadioInput(),
        choices=[("yes", "Yes"), ("no", "No")],
        coerce=lambda x: x == "yes",
        validators=[InputRequired(message="Select yes if the Fund can be applied for in Welsh")],
    )

    funding_type = RadioField(
        "What application process does this grant use?",
        widget=GovRadioInput(),
        choices=[(ft.value, ft.name) for ft in FundingType],
        validators=[DataRequired(message="Select an application process for the grant")],
    )

    prospectus_link = StringField(
        "What is the fund's prospectus link?",
        widget=GovTextInput(),
        validators=[DataRequired("Enter a prospectus link for the grant")],
    )

    ggis_reference = StringField(
        "GGIS reference",
        widget=GovTextInput(),
        validators=[DataRequired(message="Enter a GGIS reference for the grant")],
    )
    submit = SubmitField("Continue", widget=GovSubmitInput())


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
