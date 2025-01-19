from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextArea, GovTextInput
from wtforms.fields.choices import RadioField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

from proto.common.data.models import ApplicationQuestion, ProtoApplication
from proto.common.data.models.question_bank import QuestionType
from proto.common.data.services.applications import get_current_answer_to_question


def build_question_form(application: "ProtoApplication", question: ApplicationQuestion) -> FlaskForm:
    # Build the form class and attach a field for it that renders the question correctly.
    class DynamicQuestionForm(FlaskForm):
        submit = SubmitField(_l("Continue"), widget=GovSubmitInput())

    match question.type:
        case QuestionType.TEXT_INPUT:
            field = StringField(
                label=question.title, description=question.hint, widget=GovTextInput(), validators=[DataRequired()]
            )
        case QuestionType.TEXTAREA:
            field = StringField(
                label=question.title, description=question.hint, widget=GovTextArea(), validators=[DataRequired()]
            )
        case QuestionType.RADIOS:
            field = RadioField(
                label=question.title, description=question.hint, widget=GovRadioInput(), validators=[DataRequired()]
            )
            # TODO: add choices 👀
        case _:
            raise Exception("Unable to generate dynamic form for question type {_}")

    DynamicQuestionForm.question = field

    # Populate form with existing answer (if any) from the DB
    form = DynamicQuestionForm(data={"question": get_current_answer_to_question(application, question)})

    return form
