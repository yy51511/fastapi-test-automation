import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "", "description": "normal"},
        {"title": "a" * 256, "description": "normal"},
        {"title": "normal", "description": "a" * 256},
    ],
)
def test_create_item_invalid_boundary(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    payload: dict[str, str],
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=payload,
    )

    assert response.status_code == 422


def test_create_item_title_max_length(
    client: TestClient,
    superuser_token_headers: dict[str, str],
) -> None:
    payload = {
        "title": "a" * 255,
        "description": "boundary test",
    }

    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=payload,
    )

    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]


def test_read_items_with_invalid_token(client: TestClient) -> None:
    headers = {
        "Authorization": "Bearer invalid-token"
    }

    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=headers,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Could not validate credentials"