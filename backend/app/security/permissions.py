
# APPLICATION ROLES

ROLE_ADMIN = "admin"
ROLE_MANAGER = "manager"
ROLE_USER = "user"


# ============================================================
# PERMISSIONS
# ============================================================

UPLOAD_DOCUMENT = "upload_document"
VIEW_DOCUMENT = "view_document"
DELETE_DOCUMENT = "delete_document"

MANAGE_USERS = "manage_users"
VIEW_AUDIT_LOGS = "view_audit_logs"


# ============================================================
# ROLE → PERMISSIONS
# ============================================================

ROLE_PERMISSIONS: dict[str, set[str]] = {
    ROLE_ADMIN: {
        UPLOAD_DOCUMENT,
        VIEW_DOCUMENT,
        DELETE_DOCUMENT,
        MANAGE_USERS,
        VIEW_AUDIT_LOGS,
    },

    ROLE_MANAGER: {
        UPLOAD_DOCUMENT,
        VIEW_DOCUMENT,
        DELETE_DOCUMENT,
    },

    ROLE_USER: {
        UPLOAD_DOCUMENT,
        VIEW_DOCUMENT,
    },
}


# ============================================================
# CHECK PERMISSION
# ============================================================

def has_permission(
    role: str,
    permission: str,
) -> bool:
    """
    Check whether a role has a specific permission.
    """

    permissions = ROLE_PERMISSIONS.get(role, set())

    return permission in permissions