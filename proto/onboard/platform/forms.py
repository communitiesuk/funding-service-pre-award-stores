from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import (
    GovCheckboxesInput,
    GovRadioInput,
    GovSubmitInput,
    GovTextInput,
)
from wtforms import RadioField, SelectMultipleField, StringField, SubmitField
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
    submit = SubmitField("Create grant", widget=GovSubmitInput())


class CreateRoundForm(FlaskForm):
    code = StringField("Grant code", widget=GovTextInput(), validators=[DataRequired(message="Enter a grant code")])

    title = StringField(
        "Grant title", widget=GovTextInput(), validators=[DataRequired(message="Enter a title for the grant")]
    )
    title_cy = StringField("Grant title (Welsh)", widget=GovTextInput(), validators=[Optional()])

    # fixme: re-enable these, govuk-frontend-wtf datefield doesn't seem to be working - must be me doing something bad
    # proto_start_date = DateField(
    #     "When will applications open for the round?",
    #     widget=GovDateInput(),
    #     validators=[DataRequired(message="Enter a start date for the round")],
    # )
    # proto_end_date = DateField(
    #     "When will applications close for the round?",
    #     widget=GovDateInput(),  # FIXME: govuk-frontend-wtf doesn't have datetime support, ohno
    #     validators=[DataRequired(message="Enter an end date for the round")],
    # )
    submit = SubmitField("Create round", widget=GovSubmitInput())


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
