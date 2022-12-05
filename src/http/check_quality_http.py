def check_type_id(json_payload: dict[str, any]) -> None:
    """
    Check if the field type_id is present, formatted correctly and the value is respecting the specifications

    :raise TypeError: must be an integer
    :raise ValueError: must be positive
    :raise KeyError: must be present
    """
    if 'type_id' not in json_payload.keys():
        raise KeyError("The payload should contain the field type_id with an integer value")
    elif not isinstance(json_payload['type_id'], int):
        raise TypeError('The field type_id should be an int')
    elif json_payload['type_id'] <= 0:
        raise ValueError("The field type_id should be greater than 0")


def check_word_value(json_payload: dict[str, any]) -> None:
    """
    Check if the field word_value is present, formatted correctly and the value is respecting the specifications

    :raise TypeError: must be a string
    :raise ValueError: must not be empty
    :raise KeyError: must be present
    """
    if 'word_value' not in json_payload.keys():
        raise KeyError("The payload should contain the field word_value")
    elif not isinstance(json_payload['word_value'], str):
        raise TypeError('The field word_value should be an string')
    elif json_payload['word_value'] == "" or json_payload['word_value'] is None:
        raise ValueError('The field word_value must not be empty or None')


def check_ordering(json_payload: dict[str, any]) -> None:
    """
    Check if the field type_id is present, formatted correctly and the value is respecting the specifications

    :raise TypeError: must be an integer
    :raise ValueError: must be positive
    :raise KeyError: must be present
    """
    if 'ordering' not in json_payload.keys():
        raise KeyError("The payload should contain the field ordering with an integer value")
    elif not isinstance(json_payload['ordering'], int):
        raise TypeError('The field type_id should be an int')


def check_word_id(json_payload: dict[str, any]) -> None:
    """
    Check if the field type_id is present, formatted correctly and the value is respecting the specifications

    :raise TypeError: must be an integer
    :raise ValueError: must be positive
    :raise KeyError: must be present
    """
    if 'word_id' not in json_payload.keys():
        raise KeyError("The payload should contain the field word_id with an integer value")
    elif not isinstance(json_payload['word_id'], int):
        raise TypeError('The field word_id should be an int')
    elif json_payload['word_id'] <= 0:
        raise ValueError("The field word_id should be greater than 0")
