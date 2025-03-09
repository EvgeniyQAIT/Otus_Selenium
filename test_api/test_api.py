import time
import pytest
import requests

base_url = 'https://reqres.in/api'

@pytest.mark.parametrize(
    "endpoint, payload, expected_status, expected_response",
    [
        ("/register", {"email": "eve.holt@reqres.in", "password": "pistol"}, 200, lambda r: "token" in r),
        ("/register", {"email": "sydney@fife"}, 400, lambda r: r["error"] == "Missing password")
    ],
    ids=["Позитивная регистрация пользователя[200]", "Негативная регистрация пользователя[400]"]
)
def test_api_register_user(endpoint, payload, expected_status, expected_response):
    response = requests.post(f"{base_url}{endpoint}", json=payload)
    assert response.status_code == expected_status
    assert expected_response(response.json())

@pytest.mark.parametrize(
    "endpoint, payload, expected_status, expected_response",
    [
        ("/login", {"email": "eve.holt@reqres.in", "password": "cityslicka"}, 200, lambda r: "token" in r and r["token"] == "QpwL5tke4Pnpja7X4"),
        ("/login", {"email": "peter@klaven"}, 400, lambda r: r["error"] == "Missing password"),
    ],
    ids=["Позитивная авторизация пользователя[200]", "Негативная авторизация пользователя[400]"]
)
def test_api_login_user(endpoint, payload, expected_status, expected_response):
    response = requests.post(f"{base_url}{endpoint}", json=payload)
    assert response.status_code == expected_status
    assert expected_response(response.json())

@pytest.mark.parametrize(
    "endpoint, expected_status, expected_response",
    [
        ("/user/2", 200, lambda r: r.get("data") is not None),
        ("/user/23", 404, lambda r: r == {}),
    ],
    ids=["Позитивное получение данных пользователя[200]", "Негативное получение данных пользователя[404]"]
)
def test_api_get_user(endpoint, expected_status, expected_response):
    response = requests.get(f"{base_url}{endpoint}")
    assert response.status_code == expected_status
    assert expected_response(response.json())

@pytest.mark.parametrize(
    "endpoint, method, payload, expected_status, expected_response",
    [
        ("/users/2", "PUT", {"name": "morpheus", "job": "zion resident"}, 200, lambda r: r["name"] == "morpheus" and r["job"] == "zion resident"),
        ("/users/2", "PATCH", {"name": "morpheus", "job": "zion resident"}, 200, lambda r: r["name"] == "morpheus" and r["job"] == "zion resident"),
    ],
    ids=["Позитивное обновление пользователя методом PUT[200]", "Позитивное обновление пользователя методом PATCH[200]"]
)
def test_api_update_user(endpoint, method, payload, expected_status, expected_response):
    url = f"{base_url}{endpoint}"
    if method == "PUT":
        response = requests.put(url, json=payload)
    elif method == "PATCH":
        response = requests.patch(url, json=payload)
    assert response.status_code == expected_status
    assert expected_response(response.json())

@pytest.mark.parametrize(
    "endpoint, expected_status, expected_response",
    [
        ("/users?page=2", 200, lambda r: len(r["data"]) == 6 and r["page"] == 2),
        ("/users?delay=3", 200, lambda r: "data" in r),
    ],
    ids=["Позитивное получение списка пользователей на 2 странице[200]", "Позитивное получение пользователей с задержкой[200]"]
)
def test_api_get_users(endpoint, expected_status, expected_response):
    url = f"{base_url}{endpoint}"
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    assert response.status_code == expected_status
    assert expected_response(response.json())
    if "delay" in url:
        assert (end_time - start_time) >= 3

@pytest.mark.parametrize(
    "endpoint, payload, expected_status, expected_response",
    [
        ("/unknown/2", None, 200, lambda r: r["data"]["id"] == 2 and r["data"]["name"] == "fuchsia rose"),
        ("/unknown/23", None, 404, lambda r: r == {}),
        ("/unknown/2", {"name": "cerulean", "year": 2000, "color": "#98B2D1", "pantone_value": "15-4020"}, 200, lambda r: r["name"] == "cerulean"),
    ],
    ids=["Получение информации о неизвестном ресурсе[200]", "Неуспешное получение информации о неизвестном ресурсе[404]", "Обновление информации о неизвестном ресурсе[200]"]
)
def test_api_unknown_resource(endpoint, payload, expected_status, expected_response):
    url = f"{base_url}{endpoint}"
    if payload:
        response = requests.put(url, json=payload)
    else:
        response = requests.get(url)
    assert response.status_code == expected_status
    if response.content:
        assert expected_response(response.json())

def test_api_logout_user():
    """
    Тест на выход пользователя из системы
    """
    register_endpoint = f"{base_url}/logout"
    response = requests.post(register_endpoint)
    assert response.status_code == 200
    assert response.json() == {}

def test_api_delete_user():
    """
    Тест на удаление пользователя
    """
    register_endpoint = f"{base_url}/users/2"
    response = requests.delete(register_endpoint)
    assert response.status_code == 204
    assert response.text == ""

def test_api_new_user():
    """
    Тест на создание нового пользователя
    """
    register_endpoint = f"{base_url}/users"
    payload = {
        "name": "morpheus",
        "job": "leader"
    }
    response = requests.post(register_endpoint, json=payload)
    assert response.status_code == 201
    user_data = response.json()
    assert "name" in user_data
    assert "job" in user_data
    assert "id" in user_data
    assert "createdAt" in user_data
    assert user_data["name"] == "morpheus"
    assert user_data["job"] == "leader"

def test_api_delete_unknown_resource():
    """
    Тест на удаление информации о неизвестном ресурсе с ID 2
    """
    register_endpoint = f"{base_url}/unknown/2"
    response = requests.delete(register_endpoint)
    assert response.status_code == 204
    assert response.text == ""

def test_api_all_unknown_resources():
    """
    Тест на получение информации о всех неизвестных ресурсах
    """
    register_endpoint = f"{base_url}/unknown"
    response = requests.get(register_endpoint)
    assert response.status_code == 200
    data = response.json().get("data")
    assert data is not None
    assert len(data) == 6
    for item in data:
        assert "id" in item
        assert "name" in item
        assert "year" in item
        assert "color" in item
        assert "pantone_value" in item
    assert response.json().get("page") == 1

