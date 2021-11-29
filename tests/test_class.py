import pytest
from models import Order, Brewery, Breweries_names


def test_Order():
    # previous_order
    assert Order(user_client="Joao", order_value=1.2, previous_order=False)
    assert Order(user_client="Joao", order_value=1.2, previous_order="n")
    assert Order(user_client="Joao", order_value=1.2, previous_order=True)
    assert Order(user_client="Joao", order_value=1.2, previous_order="y")

    # order_value
    assert Order(user_client="Joao", order_value=0, previous_order="y")
    assert Order(user_client="Joao", order_value=1502, previous_order="y")
    assert Order(user_client="Joao", order_value=3.3, previous_order="y")
    with pytest.raises(ValueError):
        Order(user_client="Joao", order_value=-1, previous_order=True)
    with pytest.raises(ValueError):
        Order(user_client="Joao", order_value="a", previous_order=True)

    # user_client
    assert Order(user_client="Joao", order_value=0, previous_order=True)
    assert Order(user_client="Bruna", order_value=0, previous_order=True)
    assert Order(user_client="Maria", order_value=0, previous_order=True)
    assert Order(user_client="Juan", order_value=0, previous_order=True)
    with pytest.raises(ValueError):
        Order(user_client="João", order_value=0, previous_order=True)
    with pytest.raises(ValueError):
        Order(user_client="José", order_value=0, previous_order=True)
    with pytest.raises(ValueError):
        Order(user_client=1234, order_value=0, previous_order=True)
    with pytest.raises(ValueError):
        Order(user_client=5.5, order_value=0, previous_order=True)

def test_Brewery():

    assert Brewery(name="12 West Brewing Company - Production Facility")
    assert Brewery(name="12 West Brewing Company - Production Facility.")
    with pytest.raises(ValueError):
        Brewery(name="12' West Brewing Company - Production Facility.")
    with pytest.raises(ValueError):
        Brewery(name="12' West Brewing Company - Production Facility.")
