from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from backend.app.database.models import User
from backend.app.security.dependencies import get_current_user
from backend.app.security.permissions import Permission
from backend.app.security.rbac import require_permission


app = FastAPI()


# ----------------------------------------------------------
# ASK QUESTION endpoint
# ----------------------------------------------------------

@app.get("/test/ask-question")
def test_ask_question(
    current_user: Annotated[
        User,
        Depends(
            require_permission(
                Permission.ASK_QUESTION
            )
        ),
    ],
):
    return {
        "message": "Access granted",
        "user": current_user.full_name,
        "role": current_user.role,
    }


# ----------------------------------------------------------
# MANAGE USERS endpoint
# ----------------------------------------------------------

@app.get("/test/manage-users")
def test_manage_users(
    current_user: Annotated[
        User,
        Depends(
            require_permission(
                Permission.MANAGE_USERS
            )
        ),
    ],
):
    return {
        "message": "Access granted",
        "user": current_user.full_name,
        "role": current_user.role,
    }


if __name__ == "__main__":
    print("RBAC API test application created.")