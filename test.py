import pytest
import requests

API = "http://127.0.0.1:5000/billetera"

# test case para una cuenta que no exista
def test_contactos():
    response = requests.get(API + "/contactos/?minumero=1234567890")
    assert response.status_code == 404


# test case para un pago con saldo insuficiente
def test_pagar():
    response = requests.get(API + "/pagar/?minumero=123&numerodestino=456&valor=1000")
    assert response.status_code == 406

# test case para un pago a una cuenta que no está en los contactos
def test_pagar2():
    response = requests.get(API + "/pagar/?minumero=456&numerodestino=123&valor=100")
    assert response.status_code == 404

# test case para un listado de contactos correcto
def test_contactos_good():
    response = requests.get(API + "/contactos/?minumero=21345")
    assert response.status_code == 200
    assert response.json() == {
        "Luisa": "123",
        "Andrea": "456"
    }
