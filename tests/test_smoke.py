"""
Test de humo para validar la infraestructura de QA.

Este test no depende de un servidor propio; usa httpbin.org,
un servicio publico y estable disenado para pruebas HTTP.
"""

import requests


def test_public_api_is_reachable():
    """Verifica conectividad HTTP basica desde el entorno de ejecucion."""
    response = requests.get("https://httpbin.org/status/200", timeout=10)
    assert response.status_code == 200


def test_public_api_returns_json():
    """Verifica que el entorno puede parsear respuestas JSON."""
    response = requests.get("https://httpbin.org/get", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
