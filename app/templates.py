from fastapi.templating import Jinja2Templates
from typing import Any
import logging

def is_authenticated(user: Any) -> bool:
        try:
            if not user:
                return False
            return getattr(user, 'role', 'PUBLIC') != 'PUBLIC'
        except Exception as e:
            logging.warning(f"Error checking authentication: {str(e)}")
            return False


def is_admin(user: Any) -> bool:
    try:
        if not user:
            return False
        return getattr(user, 'role', 'PUBLIC') == 'ADMIN'
    except Exception as e:
        logging.warning(f"Error checking authentication: {str(e)}")
        return False


def is_user(user: Any) -> bool:
    try:
        if not user:
            return False
        return getattr(user, 'role', 'PUBLIC') == 'USER'
    except Exception as e:
        logging.warning(f"Error checking authentication: {str(e)}")
        return False


def patch_templates():
       """Jinja2Templates to automatically add context."""
       original = Jinja2Templates.TemplateResponse
       def patched_response(self, name: str, context: dict, **kwargs):
           try:
               context = context.copy() if context else {}
               request = context.get('request')
               if request:
                   user=getattr(request.state, 'user', None)
                   logging.error(user)
                   context.setdefault('current_user', getattr(request.state, 'user', None))
                   context.setdefault('is_authenticated', is_authenticated(request.state))
                   context.setdefault('is_admin', is_admin(request.state))
                   context.setdefault('is_user', is_user(request.state))


               return original(self, name, context, **kwargs)
           except Exception as e:
               logging.error(f"Error while patching a template: {str(e)}")
               raise
       Jinja2Templates.TemplateResponse = patched_response
   

