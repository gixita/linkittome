import pytest
from src.http import check_quality_http as quality


def test_check_type_id():
    json_payload = {"type": "all_words"}
    with pytest.raises(KeyError, match="The payload should contain the field type_id with an integer value"):
        quality.check_type_id(json_payload)
    json_payload = {"type_id": "all_words"}
    with pytest.raises(TypeError, match="The field type_id should be an int"):
        quality.check_type_id(json_payload)
    json_payload = {"type_id": 0}
    with pytest.raises(ValueError, match="The field type_id should be greater than 0"):
        quality.check_type_id(json_payload)


def test_check_word_value():
    json_payload = {"word": "all_words"}
    with pytest.raises(KeyError, match="The payload should contain the field word_value"):
        quality.check_word_value(json_payload)
    json_payload = {"word_value": 0}
    with pytest.raises(TypeError, match='The field word_value should be an string'):
        quality.check_word_value(json_payload)
    json_payload = {"word_value": ""}
    with pytest.raises(ValueError, match='The field word_value must not be empty or None'):
        quality.check_word_value(json_payload)


def test_check_ordering():
    json_payload = {"ordering2": "all_words"}
    with pytest.raises(KeyError, match="The payload should contain the field ordering with an integer value"):
        quality.check_ordering(json_payload)
    json_payload = {"ordering": ""}
    with pytest.raises(TypeError, match='The field type_id should be an int'):
        quality.check_ordering(json_payload)


def test_check_word_id():
    json_payload = {"word_": "all_words"}
    with pytest.raises(KeyError, match="The payload should contain the field word_id with an integer value"):
        quality.check_word_id(json_payload)
    json_payload = {"word_id": "all_words"}
    with pytest.raises(TypeError, match='The field word_id should be an int'):
        quality.check_word_id(json_payload)
    json_payload = {"word_id": 0}
    with pytest.raises(ValueError, match="The field word_id should be greater than 0"):
        quality.check_word_id(json_payload)
