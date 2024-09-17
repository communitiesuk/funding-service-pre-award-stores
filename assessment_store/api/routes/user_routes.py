from db.queries.assessment_records.queries import create_user_application_association
from db.queries.assessment_records.queries import get_metadata_for_application
from db.queries.assessment_records.queries import get_user_application_associations
from db.queries.assessment_records.queries import (
    update_user_application_association as update_user_application_association_db,
)
from db.schemas.schemas import AllocationAssociationSchema
from flask import abort
from flask import current_app
from flask import request
from fsd_utils.config.notify_constants import NotifyConstants
from services.data_services import send_notification_email


def get_all_users_associated_with_application(application_id, active=None):
    """Fetches all users associated with a given application.

    Parameters:
        application_id (str): UUID of the application.
        active (bool, optional): Filter for active associations. Defaults to None.

    Returns:
        list: Serialized list of user associations.

    Raises:
        404: If no users are found for the given application.

    """
    associations = get_user_application_associations(application_id=application_id, active=active)
    if associations:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(associations, many=True)

    current_app.logger.error(f"Could not find any users associated with application {application_id}")
    abort(404)


def get_user_application_association(application_id, user_id):
    """Fetches the association between a given user and application.

    Parameters:
        application_id (str): UUID of the application.
        user_id (str): UUID of the user.

    Returns:
        dict: Serialized user application association.

    Raises:
        404: If no association is found between the user and the application.

    """
    association = get_user_application_associations(application_id=application_id, user_id=user_id)

    if association:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(association[0])

    current_app.logger.error(f"Could not find association between {user_id} and application {application_id}")
    abort(404)


def add_user_application_association(application_id, user_id):
    """Creates a new association between a user and an application.

    Parameters:
        application_id (str): UUID of the application.
        user_id (str): UUID of the user.

    Returns:
        dict: Serialized new user application association.

    Raises:
        404: If the association cannot be created.

    """
    args = request.get_json()
    if "assigner_id" not in args:
        abort(400, "Post body must contain assigner_id field")

    send_email = args.get("send_email")
    association = create_user_application_association(
        application_id=application_id, user_id=user_id, assigner_id=args["assigner_id"]
    )

    if association:
        if send_email:
            application = get_metadata_for_application(application_id)
            send_notification_email(
                application=application,
                user_id=user_id,
                template=NotifyConstants.TEMPLATE_TYPE_ASSESSMENT_APPLICATION_ASSIGNED,
                assigner_id=args["assigner_id"],
                message=args.get("email_content"),
            )

        serialiser = AllocationAssociationSchema()
        return serialiser.dump(association), 201

    current_app.logger.error(f"Could not create association between {user_id} and application {application_id}")
    abort(404)


def update_user_application_association(application_id, user_id):
    """Updates the active status of an association between a user and an
    application.

    Parameters:
        application_id (str): UUID of the application.
        user_id (str): UUID of the user.

    Returns:
        dict: Serialized updated user application association.

    Raises:
        400: If the 'active' parameter is missing in the request.
        404: If the association cannot be updated.

    """
    args = request.get_json()
    if "active" not in args:
        abort(400, "Body must contain active field")

    if "assigner_id" not in args:
        abort(400, "Post body must contain assigner_id field")

    send_email = args.get("send_email")
    active = args.get("active")
    association = update_user_application_association_db(
        application_id=application_id, user_id=user_id, active=active, assigner_id=args["assigner_id"]
    )

    if association:
        if send_email:
            application = get_metadata_for_application(application_id)
            send_notification_email(
                application=application,
                user_id=user_id,
                template=NotifyConstants.TEMPLATE_TYPE_ASSESSMENT_APPLICATION_ASSIGNED
                if active
                else NotifyConstants.TEMPLATE_TYPE_ASSESSMENT_APPLICATION_UNASSIGNED,
                assigner_id=args["assigner_id"],
                message=args.get("email_content"),
            )

        serialiser = AllocationAssociationSchema()
        return serialiser.dump(association)

    current_app.logger.error(f"Could not update association between {user_id} and application {application_id}")
    abort(404)


def get_all_applications_associated_with_user(user_id, active=None):
    """Fetches all applications associated with a given user.

    Parameters:
        user_id (str): UUID of the user.
        active (bool, optional): Filter for active associations. Defaults to None.

    Returns:
        list: Serialized list of application associations.

    Raises:
        404: If no applications are found for the given user.

    """
    associations = get_user_application_associations(user_id=user_id, active=active)
    if associations:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(associations, many=True)

    current_app.logger.error(f"Could not find any applications associated with user {user_id}")
    abort(404)


def get_all_associations_assigned_by_user(assigner_id, active=None):
    """Fetches all associations where the user is the assigner.

    Parameters:
        assigner_id (str): UUID of the assigner.
        active (bool, optional): Filter for active associations. Defaults to None.

    Returns:
        list: Serialized list of application associations.

    Raises:
        404: If no applications are found for the given user.

    """
    associations = get_user_application_associations(assigner_id=assigner_id, active=active)
    if associations:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(associations, many=True)

    current_app.logger.error(f"Could not find any applications assigned by user {assigner_id}")
    abort(404)
