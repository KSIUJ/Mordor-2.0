from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Any
import logging

class TemplateMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, templates_dir: str = "templates"):
        super().__init__(app)
        self.templates = Jinja2Templates(directory=templates_dir)
        self._patch_templates()

    def _patch_templates(self):
        """Jinja2Templates to automatically add context."""
        original = Jinja2Templates.TemplateResponse
        is_authenticated = self._is_authenticated
        def patched_response(self, name: str, context: dict, **kwargs):
            try:
                context = context.copy() if context else {}
                
                request = context.get('request')
                if request:
                    context.setdefault('current_user', getattr(request.state, 'user', None))
                    context.setdefault('is_authenticated', is_authenticated(getattr(request.state, 'user', None)))
                    
                
                return original(self, name, context, **kwargs)
            except Exception as e:
                logging.error(f"Error in template middleware: {str(e)}")
                raise

        Jinja2Templates.TemplateResponse = patched_response

    def _is_authenticated(self, user: Any) -> bool:
        try:
            if not user:
                return False
            return (getattr(user, 'role', 'PUBLIC') != 'PUBLIC')
        except Exception as e:
            logging.warning(f"Error checking authentication: {str(e)}")
            return False

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        return response