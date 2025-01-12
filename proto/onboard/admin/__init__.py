from proto.onboard.admin.entities import (
    DataStandardAdmin,
    FundAdmin,
    RoundAdmin,
    TemplateQuestionAdmin,
    TemplateSectionAdmin,
)


def register_admin_views(flask_admin, db):
    flask_admin.add_view(FundAdmin(db.session))
    flask_admin.add_view(RoundAdmin(db.session))
    flask_admin.add_view(DataStandardAdmin(db.session, category="Templates"))
    flask_admin.add_view(TemplateSectionAdmin(db.session, category="Templates"))
    flask_admin.add_view(TemplateQuestionAdmin(db.session, category="Templates"))
