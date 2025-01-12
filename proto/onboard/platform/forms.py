from flask_babel import lazy_gettext as _l
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
    code = StringField(
        _l("Grant code"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a grant code"))]
    )

    name = StringField(
        _l("Grant name"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a name for the grant"))]
    )
    name_cy = StringField(_l("Grant name (Welsh)"), widget=GovTextInput(), validators=[Optional()])

    title = StringField(
        _l("Grant title"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a title for the grant"))]
    )
    title_cy = StringField(_l("Grant title (Welsh)"), widget=GovTextInput(), validators=[Optional()])

    description = StringField(
        _l("Grant description"),
        widget=GovTextInput(),
        validators=[DataRequired(message=_l("Enter a description for the grant"))],
    )
    description_cy = StringField(_l("Grant description (Welsh)"), widget=GovTextInput(), validators=[Optional()])

    welsh_available = RadioField(
        _l("Welsh available?"),
        widget=GovRadioInput(),
        choices=[("yes", _l("Yes")), ("no", _l("No"))],
        coerce=lambda x: x == "yes",
        validators=[InputRequired(message=_l("Select yes if the Fund can be applied for in Welsh"))],
    )

    funding_type = RadioField(
        _l("What application process does this grant use?"),
        widget=GovRadioInput(),
        choices=[(ft.value, ft.name) for ft in FundingType],
        validators=[DataRequired(message=_l("Select an application process for the grant"))],
    )

    prospectus_link = StringField(
        _l("What is the fund's prospectus link?"),
        widget=GovTextInput(),
        validators=[DataRequired(_l("Enter a prospectus link for the grant"))],
    )

    ggis_reference = StringField(
        _l("GGIS reference"),
        widget=GovTextInput(),
        validators=[DataRequired(message=_l("Enter a GGIS reference for the grant"))],
    )
    submit = SubmitField(_l("Create grant"), widget=GovSubmitInput())


class CreateRoundForm(FlaskForm):
    code = StringField(
        _l("Grant code"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a grant code"))]
    )

    title = StringField(
        _l("Grant title"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a title for the grant"))]
    )
    title_cy = StringField(_l("Grant title (Welsh)"), widget=GovTextInput(), validators=[Optional()])

    # fixme: re-enable these, govuk-frontend-wtf datefield doesn't seem to be working - must be me doing something bad
    # proto_start_date = DateField(
    #     _l("When will applications open for the round?"),
    #     widget=GovDateInput(),
    #     validators=[DataRequired(message=_l("Enter a start date for the round"))],
    # )
    # proto_end_date = DateField(
    #     _l("When will applications close for the round?"),
    #     widget=GovDateInput(),  # FIXME: govuk-frontend-wtf doesn't have datetime support, ohno
    #     validators=[DataRequired(message=_l("Enter an end date for the round"))],
    # )
    submit = SubmitField(_l("Create round"), widget=GovSubmitInput())


class ChooseTemplateSectionsForm(FlaskForm):
    sections = SelectMultipleField(
        _l("Choose templates from the question bank"),
        widget=GovCheckboxesInput(),
        validators=[],
    )
    submit = SubmitField(_l("Continue"), widget=GovSubmitInput())

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
