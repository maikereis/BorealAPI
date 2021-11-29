import pytest
from datetime import datetime
from security.models import Token, TokenOwner, JWTPayload


def test_Token():
    assert Token(access_token="13234235fsdfsdfsdfds", token_type='asfdasdasdasd')
    assert Token(access_token="fsdfsdfsdfds", token_type='asfdasdasdasd')
    with pytest.raises(ValueError):
        Token(access_token="fsdfsdfsdfds", token_type='342423asfdasdasdasd')
    with pytest.raises(ValueError):
        Token(access_token=13124134, token_type='342423asfdasdasdasd')
    with pytest.raises(ValueError):
        Token(access_token=13124134, token_type=11343)

def test_TokenOwner():
    assert TokenOwner(email="fulano@gmail.com")
    assert TokenOwner(email="fulano@uol.uol.com")
    assert TokenOwner(email="my_first_name.something@uol.uol.com")
    with pytest.raises(ValueError):
        TokenOwner(email="121234132@uol.uol.com")
    with pytest.raises(ValueError):
        TokenOwner(email="my_first_name.something@112344")

def test_JWTPayload():
    assert JWTPayload(sub="fulano@gmail.com", exp=datetime.utcnow())
    assert JWTPayload(sub="fulano@gmail.com", exp='2021-10-23T02:24:55.243Z')
    assert JWTPayload(sub="fulano@gmail.com", exp='2021-10-23T02:24:55')
    assert JWTPayload(sub="fulano@gmail.com", exp='2021-10-23T02:24')

    with pytest.raises(ValueError):
        assert JWTPayload(sub="fulano@gmail.com", exp='2021-10-23T02')
    with pytest.raises(ValueError):
        assert JWTPayload(sub="23121431", exp='2021-10-23T02')
    with pytest.raises(ValueError):
        assert JWTPayload(sub="23121431@gmail.com", exp='2021-10-23T02')




