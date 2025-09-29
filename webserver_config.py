import os
import logging
import jwt
import requests

from airflow.configuration import conf
from airflow.www.security import AirflowSecurityManager
from typing import Any, List, Union, Dict

from flask_appbuilder.security.manager import AUTH_OAUTH

log = logging.getLogger(__name__)
log.setLevel(os.getenv("AIRFLOW__LOGGING__FAB_LOGGING_LEVEL", "DEBUG"))

basedir = os.path.abspath(os.path.dirname(__file__))

# The SQLAlchemy connection string.
AUTH_TYPE = AUTH_OAUTH

AUTH_USER_REGISTRATION = True

AUTH_USER_REGISTRATION_ROLE = "Viewer"

CSRF_ENABLED = True

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = conf.get('core', 'SQL_ALCHEMY_CONN')

AUTH_ROLES_MAPPING = {
"Viewer": ["Viewer"],
"User": ["User"],
"Op": ["Op"],
f"{os.environ['AUTHENTIK_OAUTH_GROUP']}": ["Admin"],
}

OAUTH_PROVIDERS = [
    {'name': 'authentik', 'icon': 'fa-sign-in', 'token_key': 'access_token',
     'remote_app': {
         'userinfo_url': f'https://authentik.{os.environ["DOMAIN"]}/application/o/userinfo/',
         'server_metadata_url': f'https://authentik.{os.environ["DOMAIN"]}/application/o/airflow/.well-known/openid-configuration',
         'client_id': f'{os.environ["AUTHENTIK_OAUTH_CLIENT_ID"]}',
         'client_secret': f'{os.environ["AUTHENTIK_OAUTH_CLIENT_SECRET"]}',
         'api_base_url': f'https://authentik.{os.environ["DOMAIN"]}/application/o/airflow/.well-known/openid-configuration',
         'client_kwargs': {
             'scope': 'openid profile email groups',
             "verify_signature": True,
         },
         'request_token_url': None,
         'access_token_url':f'https://authentik.{os.environ["DOMAIN"]}/application/o/token/',
         'jwks_uri': f'https://authentik.{os.environ["DOMAIN"]}/application/o/airflow/jwks/',
         'authorize_url': f'https://authentik.{os.environ["DOMAIN"]}/application/o/authorize/',
         'redirect_url': f'http://airflow.destroyer.{os.environ["DOMAIN"]}/oauth-authorized/Authentik'
         }
     },
]

class CustomSecurityManager(AirflowSecurityManager):
    pass
    # def get_oauth_user_info(self, provider: str, response: Dict[str, Any]) -> Dict[str, Any]:
    #     token = response["access_token"]
    #     me = jwt.decode(token, algorithms=["HS256", "RS256"], verify=False)
    #     # me = remote_app.get("userinfo")

    #     groups = me["groups"]

    #     log.info("groups: {0}".format(groups))

    #     if not groups:
    #         groups = ["Viewer"]

    #     userinfo = {
    #         "username": me.get("preferred_username"),
    #         "email": me.get("email"),
    #         "first_name": me.get("name").split(" ")[0],
    #         "last_name": me.get("name").split(" ")[1],
    #         "role_keys": groups,
    #     }

    #     log.info("user info: {0}".format(userinfo))

    #     return userinfo

# Make sure to replace this with your own implementation of AirflowSecurityManager class
SECURITY_MANAGER_CLASS = CustomSecurityManager
