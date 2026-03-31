from app.services.auth_service import AuthService


class FakeUserRepository:
    def __init__(self, user=None):
        self.user = user
        self.checked_email = None
        self.created_payload = None

    async def get_by_email(self, email):
        self.checked_email = email
        return self.user

    async def create(self, payload):
        self.created_payload = payload
        return {
            "id": "user-123",
            "name": payload["name"],
            "email": payload["email"],
            "password": payload["password"],
            "role": payload["role"],
            "is_active": True,
        }


def test_register_creates_user_with_clean_email_and_role(run_async, payload, monkeypatch):
    service = AuthService()
    service.user_repository = FakeUserRepository()

    monkeypatch.setattr("app.services.auth_service.get_password_hash", lambda password: f"hashed::{password}")

    result = run_async(
        service.register(
            payload(
                name="Jane",
                email="  JANE@Example.com  ",
                password="secret123",
                role="  CUSTOMER  ",
            )
        )
    )

    assert result["email"] == "jane@example.com"
    assert result["role"] == "customer"
    assert "password" not in result
    assert service.user_repository.checked_email == "jane@example.com"
    assert service.user_repository.created_payload["password"] == "hashed::secret123"


def test_register_rejects_invalid_role(get_error, payload):
    service = AuthService()

    error = get_error(
        service.register(
            payload(name="Jane", email="jane@example.com", password="secret123", role="manager")
        )
    )

    assert error.status_code == 422
    assert error.detail == "Invalid role"


def test_login_returns_token_for_valid_user(run_async, payload, monkeypatch):
    service = AuthService()
    service.user_repository = FakeUserRepository(
        user={
            "id": "user-123",
            "email": "jane@example.com",
            "password": "hashed-password",
            "role": "customer",
            "is_active": True,
        }
    )

    monkeypatch.setattr("app.services.auth_service.verify_password", lambda plain, hashed: plain == "secret123")
    monkeypatch.setattr("app.services.auth_service.create_access_token", lambda subject, role: f"token-{subject}-{role}")

    result = run_async(service.login(payload(email="JANE@example.com", password="secret123")))

    assert result.access_token == "token-user-123-customer"
    assert result.token_type == "bearer"


def test_login_rejects_bad_password(get_error, payload, monkeypatch):
    service = AuthService()
    service.user_repository = FakeUserRepository(
        user={
            "id": "user-123",
            "email": "jane@example.com",
            "password": "hashed-password",
            "role": "customer",
            "is_active": True,
        }
    )

    monkeypatch.setattr("app.services.auth_service.verify_password", lambda plain, hashed: False)

    error = get_error(service.login(payload(email="jane@example.com", password="wrong-password")))

    assert error.status_code == 401
    assert error.detail == "Invalid credentials"


def test_login_rejects_inactive_user(get_error, payload, monkeypatch):
    service = AuthService()
    service.user_repository = FakeUserRepository(
        user={
            "id": "user-123",
            "email": "jane@example.com",
            "password": "hashed-password",
            "role": "customer",
            "is_active": False,
        }
    )

    monkeypatch.setattr("app.services.auth_service.verify_password", lambda plain, hashed: True)

    error = get_error(service.login(payload(email="jane@example.com", password="secret123")))

    assert error.status_code == 403
    assert error.detail == "User inactive"
