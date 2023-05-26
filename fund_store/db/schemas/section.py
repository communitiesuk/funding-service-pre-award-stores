from db.models.section import Section
from db.models.section import SectionField
from marshmallow.fields import Method
from marshmallow.fields import String
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested


class SectionFieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SectionField

    field_id = auto_field()
    display_order = auto_field()

    def get_display_type(self, obj):
        return obj.field.display_type

    def get_title(self, obj):
        return obj.field.title

    def get_field_type(self, obj):
        return obj.field.field_type

    display_type = Method("get_display_type")
    field_type = Method("get_field_type")
    title = Method("get_title")


class SectionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Section

    def get_form_name(self, obj):
        return obj.form_name[0].form_name if obj.form_name else None

    def get_weighting(self, obj):
        return obj.weighting if obj.weighting else None

    children = Nested("SectionSchema", many=True, allow_none=True)
    path = String()
    fields = Nested("SectionFieldSchema", many=True, allow_none=True)
    form_name = Method("get_form_name")
    weighting = Method("get_weighting")
