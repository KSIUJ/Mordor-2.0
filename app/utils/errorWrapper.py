from functools import wraps

from fastapi import HTTPException

#   =============== ERROR HANDLING WRAPPER ==================
def handle_file_service_errors(func):
    """Decorator for handling errors"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PermissionError as e:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to perform this action"
            )
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=409,
                detail="Users cannot modify accepted files"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )
    wrapper.__name__ = func.__name__
    wrapper.__annotations__ = func.__annotations__
    wrapper.__doc__ = func.__doc__

    return wrapper