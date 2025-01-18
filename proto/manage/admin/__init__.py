from flask_admin.menu import MenuLink

from proto.manage.admin.entities import (
    ApplicationQuestionAdmin,
    ApplicationSectionAdmin,
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
    flask_admin.add_view(ApplicationSectionAdmin(db.session, category="Applications"))
    flask_admin.add_view(ApplicationQuestionAdmin(db.session, category="Applications"))

    flask_admin.add_link(MenuLink(name="← Back to Grant management", url="/"))
