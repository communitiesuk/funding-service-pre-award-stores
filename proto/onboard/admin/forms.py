from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextInput
from wtforms.fields.choices import RadioField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import URL, DataRequired, Length, Optional

from proto.common.data.models.fund import FundingType


class CreateGrantForm(FlaskForm):
    name = StringField(
        _l("Grant name"), widget=GovTextInput(), validators=[DataRequired(_l("Enter a name for the grant"))]
    )
    name_cy = StringField(
        _l("Grant name in Welsh"),
        widget=GovTextInput(),
        validators=[Optional()],
    )
    title = StringField(
        _l("Grant title"), widget=GovTextInput(), validators=[DataRequired(_l("Enter a title for the grant"))]
    )
    short_code = StringField(
        _l("Grant code"), widget=GovTextInput(), validators=[DataRequired(_l("Enter a code for the grant"))]
    )
    funding_type = RadioField(
        _l("Grant type"),
        widget=GovRadioInput(),
        choices=[(ft.value, ft.name) for ft in FundingType],
        coerce=lambda val: FundingType(val),
        validators=[DataRequired(_l("Select a grant type"))],
    )
    ggis_scheme_reference_number = StringField(
        _l("GGIS scheme reference number"),
        widget=GovTextInput(),
        validators=[
            DataRequired(_l("Enter a GGIS scheme reference number")),
            Length(max=255, message=_l("Enter fewer than 255 characters for the GGIS scheme reference number")),
        ],
    )
    prospectus_link = StringField(
        _l("Grant type"),
        widget=GovTextInput(),
        validators=[
            DataRequired(_l("Enter a prospectus URL for the grant")),
            URL(allow_ip=False, message="Enter a valid URL for the grant"),
        ],
    )
    submit = SubmitField("Save and continue", widget=GovSubmitInput())
