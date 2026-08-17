from enum import Enum

class Permission(str, Enum):
    """
    Application permissions used by the RBAC system.
    
    These values must match the permission_name values
    in the existing PostgreSQL permissions table."""


    
    LOGIN = "LOGIN"

    ASK_QUESTION = "ASK_QUESTION"

    VIEW_DOCUMENT = "VIEW_DOCUMENT"

    UPLOAD_DOCUMENT = "UPLOAD_DOCUMENT"

    DELETE_DOCUMENT = "DELETE_DOCUMENT"

    VIEW_CHAT_HISTORY = "VIEW_CHAT_HISTORY"

    DELETE_CHAT_HISTORY = "DELETE_CHAT_HISTORY"

    VIEW_AUDIT_LOG = "VIEW_AUDIT_LOG"

    MANAGE_USERS = "MANAGE_USERS"

    MANAGE_PERMISSIONS = "MANAGE_PERMISSIONS"