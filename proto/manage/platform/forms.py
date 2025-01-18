from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import (
    GovCheckboxesInput,
    GovRadioInput,
    GovSubmitInput,
    GovTextInput,
)
from wtforms import RadioField, SelectMultipleField, StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, InputRequired, Optional, Regexp
from wtforms.widgets.core import HiddenInput

from proto.common.data.models import TemplateSection
from proto.common.data.models.fund import FundingType
from proto.common.data.models.question_bank import QuestionType


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
        _l("Round code"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a grant code"))]
    )

    title = StringField(
        _l("Round title"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a title for the grant"))]
    )
    title_cy = StringField(_l("Round title (Welsh)"), widget=GovTextInput(), validators=[Optional()])

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


class NewSectionForm(FlaskForm):
    title = StringField(
        _l("What is name of the section?"),
        widget=GovTextInput(),
        validators=[DataRequired(message=_l("Enter the name of the section"))],
    )
    slug = StringField(
        _l("What is the URL slug for this section?"),
        widget=GovTextInput(),
        validators=[
            DataRequired(message=_l("Enter a URL slug for the section")),
            Regexp(r"[a-z\-]+", message=_l("Enter a URL slug using only letters and dashes")),
        ],
        filters=[lambda val: val.lower() if val else val],
    )
    order = IntegerField(
        widget=HiddenInput(),
    )
    submit = SubmitField(_l("Add section"), widget=GovSubmitInput())


class NewQuestionForm(FlaskForm):
    type = RadioField(
        _l("What type of question are you adding?"),
        widget=GovRadioInput(),
        choices=[(ft.value, ft.name) for ft in QuestionType],
        validators=[DataRequired(message=_l("Select a question type"))],
    )
    title = StringField(
        _l("What is the question?"),
        widget=GovTextInput(),
        validators=[DataRequired(message=_l("Enter the question"))],
    )
    hint = StringField(
        _l("What is the hint text for the question?"),
        description="Only provide this if additional information is needed to help answer the question correctly.",
        widget=GovTextInput(),
        validators=[Optional()],
    )
    slug = StringField(
        _l("What is the URL slug for this question?"),
        widget=GovTextInput(),
        validators=[
            DataRequired(message=_l("Enter a URL slug for the question")),
            Regexp(r"[a-z\-]+", message=_l("Enter a URL slug using only letters and dashes")),
        ],
    )
    order = IntegerField(
        widget=HiddenInput(),
    )
    submit = SubmitField(_l("Add question"), widget=GovSubmitInput())


class MakeGrantLiveForm(FlaskForm):
    submit = SubmitField(_l("Make grant live"), widget=GovSubmitInput())


class MakeRoundLiveForm(FlaskForm):
    submit = SubmitField(_l("Make round live"), widget=GovSubmitInput())


class PreviewApplicationForm(FlaskForm):
    round_id = StringField(None, widget=HiddenInput(), validators=[DataRequired()])
    account_id = StringField(None, widget=HiddenInput(), validators=[DataRequired()])
    submit = SubmitField(None, widget=GovSubmitInput(), validators=[DataRequired()])

    def __init__(self, *args, submit_label: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.submit.label.text = submit_label
