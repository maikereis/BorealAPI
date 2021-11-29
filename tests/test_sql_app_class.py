import pytest
from sql_app.models import User, UserCreate, UserBase


def test_UserBase():
    assert UserBase(email="fulano@gmail.com")
    assert UserBase(email="fulano21@gmail.com")
    assert UserBase(email="fulano_21@gmail.com")
    with pytest.raises(ValueError):
        UserBase(email="111")
    with pytest.raises(ValueError):
        UserBase(email="111@gmail.com")


def test_UserCreate():
    assert UserCreate(password="mypass", email="fulano@gmail.com")
    assert UserCreate(password="mypasswithnumbers124", email="fulano@gmail.com")
    assert UserCreate(password="mypq", email="fulano@gmail.com")
    assert UserCreate(password="111", email="fulano@gmail.com")
    assert UserCreate(password="P4SSWORD@#!023423", email="fulano@gmail.com")


def test_User():
    assert User(password="mypass", email="fulano@gmail.com", is_active=False, id=0)
    assert User(password="mypass", email="fulano@gmail.com", is_active=True, id=1)
    assert User(password="mypass", email="fulano@gmail.com", is_active="y", id=10)
    assert User(password="mypass", email="fulano@gmail.com", is_active="n", id=1000)
    assert User(password="mypass", email="fulano@gmail.com", is_active=1, id=1)
    assert User(password="mypass", email="fulano@gmail.com", is_active=0, id=1)

    with pytest.raises(ValueError):
        User(password="mypass", email="fulano@gmail.com", is_active=False, id=-1)
