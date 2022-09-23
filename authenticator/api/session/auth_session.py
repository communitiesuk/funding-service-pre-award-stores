from datetime import datetime
from datetime import timedelta

import jwt
from api.responses import error_response
from api.session.exceptions import SessionCreateError
from config import Config
from flask import make_response
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask.views import MethodView
from models.magic_link import MagicLinkMethods
from security.utils import create_token
from security.utils import decode_with_options
from security.utils import validate_token


class AuthSessionView(MethodView):
    """
    Views for session related operations
    """

    @staticmethod
    def user():
        """
        GET /sessions/user endpoint
        Shows the user details of the current user session
        or an error if no authenticated user session found
        :return: 200 user details json or 404 error
        """
        token = request.cookies.get(Config.FSD_USER_TOKEN_COOKIE_NAME)
        if token:
            try:
                valid_token = validate_token(token)
                return make_response(valid_token), 200
            except jwt.PyJWTError:
                error_response(404, "Session token expired or invalid")
        error_response(404, "No session token found")

    @staticmethod
    def clear_session():
        """
        Clears the user session (signing them out)
        Also deletes an existing jwt auth cookie and removes the corresponding
        link records from redis

        Returns: 302 redirect to signed-out page
        """
        existing_auth_token = request.cookies.get(
            Config.FSD_USER_TOKEN_COOKIE_NAME
        )
        status = "no_token"
        valid_token = False
        if existing_auth_token:
            # Check if token is valid
            try:
                valid_token = validate_token(existing_auth_token)
                status = "sign_out_request"
            except jwt.ExpiredSignatureError:
                valid_token = decode_with_options(
                    existing_auth_token, options={"verify_exp": False}
                )
                status = "expired_token"
            except jwt.PyJWTError:
                status = "invalid_token"

            # If validly issued token, clear the redis store
            # of the account and link record
            if valid_token and isinstance(valid_token, dict):
                MagicLinkMethods().clear_existing_user_record(
                    valid_token.get("accountId")
                )

        # Clear the session
        session.clear()

        # Clear the cookie and redirect to signed out page
        signed_out_url = url_for("magic_links_bp.signed_out", status=status)
        response = make_response(redirect(signed_out_url), 302)
        response.set_cookie(
            Config.FSD_USER_TOKEN_COOKIE_NAME,
            "",
            domain=Config.COOKIE_DOMAIN,
            expires=0,
            secure=Config.SESSION_COOKIE_SECURE,
            samesite=Config.SESSION_COOKIE_SAMESITE,
            httponly=Config.SESSION_COOKIE_HTTPONLY,
        )
        return response

    @classmethod
    def create_session_and_redirect(cls, account_id: str, redirect_url: str):
        """
        Sets a user session token in the client for a given account_id
        and then redirects to a given url
        :param account_id: The account_id of the user we are authenticating
        :param redirect_url: The url to redirect them to after session creation
        :return: 302 redirect
        """
        try:
            session_details = cls.create_session_details_with_token(account_id)
            response = make_response(redirect(redirect_url), 302)
            expiry = datetime.now() + timedelta(
                seconds=Config.FSD_SESSION_TIMEOUT_SECS
            )
            response.set_cookie(
                Config.FSD_USER_TOKEN_COOKIE_NAME,
                session_details["token"],
                domain=Config.COOKIE_DOMAIN,
                expires=expiry,
                secure=Config.SESSION_COOKIE_SECURE,
                samesite=Config.SESSION_COOKIE_SAMESITE,
                httponly=Config.SESSION_COOKIE_HTTPONLY,
            )
            return response
        except SessionCreateError as e:
            error_response(404, str(e))

    @classmethod
    def create_session_details_with_token(cls, account_id: str):
        """
        Creates a signed expiring session token for the given account_id
        :param account_id: The account_id for the user to create a token for
        :return: A dict including the signed session token
        """
        session_details = {
            "accountId": account_id,
            "iat": int(datetime.now().timestamp()),
            "exp": int(
                datetime.now().timestamp() + Config.FSD_SESSION_TIMEOUT_SECS
            ),
        }

        session_details.update({"token": create_token(session_details)})
        session.update(session_details)
        return session_details
