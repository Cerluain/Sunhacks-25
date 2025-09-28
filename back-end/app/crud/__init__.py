"""app.crud package exports.

Expose individual CRUD modules as attributes so callers can do:

	from app import crud
	crud.user.get_by_email(...)

This keeps compatibility with existing code that expects `app.crud.user`.
"""

from . import crud_user as user
from . import crud_item as item

__all__ = ["user", "item"]
