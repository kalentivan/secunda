import requests
from uuid import UUID

from src.core.config import settings
from .conftest import BASE_URL

# Предполагаемые ID из fixtures.json
BUILDING_ID = "550e8400-e29b-41d4-a716-446655440001"
ACTIVITY_ID = "550e8400-e29b-41d4-a716-446655440103"  # Мясная продукция
ROOT_ACTIVITY_ID = "550e8400-e29b-41d4-a716-446655440101"  # Еда
ORGANIZATION_ID = "550e8400-e29b-41d4-a716-446655440201"  # ООО Рога и Копыта

# Заголовки с API-ключом
HEADERS = {"X-API-Key": settings.SECRET_KEY}


def test_get_organizations_by_building():
    """Тест получения списка организаций по ID здания."""
    response = requests.get(f"{BASE_URL}/organizations/by_building/{BUILDING_ID}/", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "Новая Компания" in [_["name"] for _ in data]

    # Тест с несуществующим зданием
    response = requests.get(f"{BASE_URL}/organizations/by_building/{str(UUID(int=0))}/", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "В здании не найдены организации"


def test_get_organizations_by_activity():
    """Тест получения списка организаций по ID деятельности."""
    response = requests.get(f"{BASE_URL}/organizations/by_activity/{ACTIVITY_ID}/", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(org["id"] == ORGANIZATION_ID for org in data)

    # Тест с несуществующей деятельностью
    response = requests.get(f"{BASE_URL}/organizations/by_activity/{str(UUID(int=0))}/", headers=HEADERS)
    assert response.status_code == 404


def test_get_organizations_by_geo_radius():
    """Тест получения организаций в радиусе от точки."""
    payload = {
        "latitude": 55.7522,  # Координаты из fixtures.json (Ленина 1)
        "longitude": 37.6156,
        "radius_km": 10.0
    }
    response = requests.post(f"{BASE_URL}/organizations/by_geo/", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(org["id"] == ORGANIZATION_ID for org in data)

    # Тест с пустым радиусом (слишком далеко)
    payload["latitude"] = 0.0
    payload["longitude"] = 0.0
    response = requests.post(f"{BASE_URL}/organizations/by_geo/", json=payload, headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Не найдены здания в заданной области"


def test_get_organizations_by_geo_rectangle():
    """Тест получения организаций в прямоугольной области."""
    payload = {
        "lat_min": 55.7,
        "lat_max": 55.8,
        "lon_min": 37.5,
        "lon_max": 37.7
    }
    response = requests.post(f"{BASE_URL}/organizations/by_geo/", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(org["id"] == ORGANIZATION_ID for org in data)

    # Тест с некорректной областью
    payload["lat_min"] = 0.0
    payload["lat_max"] = 0.1
    payload["lon_min"] = 0.0
    payload["lon_max"] = 0.1
    response = requests.post(f"{BASE_URL}/organizations/by_geo/", json=payload, headers=HEADERS)
    assert response.status_code == 400


def test_get_organization_by_id():
    """Тест получения организации по ID."""
    response = requests.get(f"{BASE_URL}/organizations/{ORGANIZATION_ID}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ORGANIZATION_ID

    # Тест с несуществующей организацией
    response = requests.get(f"{BASE_URL}/organizations/{str(UUID(int=0))}", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Организация не найдена"


def test_get_organizations_by_activity_tree():
    """Тест получения организаций по дереву деятельности (Еда)."""
    response = requests.get(f"{BASE_URL}/organizations/by_activity_tree/{ROOT_ACTIVITY_ID}/", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Должны найтись организации с "Мясная продукция" и "Молочная продукция"
    assert any(org["id"] == ORGANIZATION_ID for org in data)

    # Тест с несуществующей деятельностью
    response = requests.get(f"{BASE_URL}/organizations/by_activity_tree/{str(UUID(int=0))}/", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "No organizations found for this activity tree"


def test_get_organizations_by_name():
    """Тест поиска организаций по имени."""
    response = requests.get(f"{BASE_URL}/organizations/by_name/Рога/", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["id"] == ORGANIZATION_ID

    # Тест с несуществующим именем
    response = requests.get(f"{BASE_URL}/organizations/by_name/Несуществующая/", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Не найдена организация по названию"


def test_create_organization():
    """Тест создания новой организации."""
    new_organization_id = str(UUID(int=123456789))
    payload = {
        "name": "Новая Компания",
        "building_id": BUILDING_ID,
        "phone_numbers": ["5-555-555", "6-666-666"],
        "activity_ids": [ACTIVITY_ID, "550e8400-e29b-41d4-a716-446655440104"]  # Мясная и Молочная продукция
    }
    response = requests.post(f"{BASE_URL}/organizations/", json=payload, headers=HEADERS)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["building_id"] == BUILDING_ID

    # Тест с несуществующим зданием
    payload["building_id"] = str(UUID(int=0))
    response = requests.post(f"{BASE_URL}/organizations/", json=payload, headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Здание не найдено"


def test_update_organization():
    """Тест обновления организации."""
    payload = {
        "name": "Обновленная Рога и Копыта",
        "phone_numbers": ["7-777-777"],
        "activity_ids": ["550e8400-e29b-41d4-a716-446655440104"]  # Только Молочная продукция
    }
    response = requests.patch(f"{BASE_URL}/organizations/{ORGANIZATION_ID}/", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]

    # Тест с несуществующей организацией
    response = requests.patch(f"{BASE_URL}/organizations/{str(UUID(int=0))}/", json=payload, headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Организация не найдена"


def test_delete_organization():
    """Тест мягкого удаления организации."""
    # Сначала создадим новую организацию для удаления
    payload = {
        "name": "Компания для удаления",
        "building_id": BUILDING_ID,
        "phone_numbers": ["9-999-999"],
        "activity_ids": [ACTIVITY_ID]
    }
    response = requests.post(f"{BASE_URL}/organizations/", json=payload, headers=HEADERS)
    assert response.status_code == 201
    r_data = response.json()
    # Удаляем
    response = requests.delete(f"{BASE_URL}/organizations/{r_data["id"]}/", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == data["id"]

    # Проверяем, что организация больше не доступна
    response = requests.get(f"{BASE_URL}/organizations/{r_data["id"]}", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Организация не найдена"


def test_unauthorized_access():
    """Тест доступа без API-ключа или с неверным ключом."""
    # Без ключа
    response = requests.get(f"{BASE_URL}/organizations/{ORGANIZATION_ID}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API Key"

    # С неверным ключом
    wrong_headers = {"X-API-Key": "wrong-key"}
    response = requests.get(f"{BASE_URL}/organizations/{ORGANIZATION_ID}", headers=wrong_headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API Key"
