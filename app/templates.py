from fastapi.templating import Jinja2Templates
from typing import Any
import logging

def is_authenticated(user: Any) -> bool:
        try:
            if not user:
                return False
            return (getattr(user, 'role', 'PUBLIC') != 'PUBLIC')
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
                   context.setdefault('current_user', getattr(request.state, 'user', None))
                   context.setdefault('is_authenticated', is_authenticated(getattr(request.state, 'user', None)))
                   
               
               return original(self, name, context, **kwargs)
           except Exception as e:
               logging.error(f"Error while patching a template: {str(e)}")
               raise
       Jinja2Templates.TemplateResponse = patched_response
   

