def camel_case_to_snake_case(input_str: str) -> str:
    """
    Преобразует строку в стиле CamelCase в стиль snake_case.

    >>> camel_case_to_snake_case("SomeSDK")
    'some_sdk'
    >>> camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'
    >>> camel_case_to_snake_case("SDKDemo")
    'sdk_demo'
    >>> camel_case_to_snake_case("HelloWorldTest123_Test")
    'hello_world_test123_test'
    >>> camel_case_to_snake_case("HelloWorldTest123_Test_Test")
    'hello_world_test123_test_test'
    """
    chars = []
    for c_idx, char in enumerate(input_str):
        # Если это не первая буква и символ - заглавный
        if c_idx > 0 and char.isupper():
            # Предыдущий символ
            prev_char = input_str[c_idx - 1]
            # Проверяем, не является ли предыдущий символ подчеркиванием
            if prev_char != "_":
                chars.append("_")
        # Добавляем строчную букву в список
        chars.append(char.lower())

    # Соединяем список символов в строку
    return "".join(chars)
