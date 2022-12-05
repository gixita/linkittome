def check_type_id(json: dict[str, any]) -> None:
    """
    Check if the field type_id is present, formatted correctly and the value is respecting the specifications

    :raise TypeError: must be an integer
    :raise ValueError: must be positive
    :raise KeyError: must be present
    """
    if 'type_id' not in json.keys():
        raise KeyError("The payload should contain the field type_id with an integer value")
    elif not isinstance(json['type_id'], int):
        raise TypeError('The field type_id should be an int')
    elif json['type_id'] <= 0:
        raise ValueError('The field type_id should be strictly positive (greater than 0)')
