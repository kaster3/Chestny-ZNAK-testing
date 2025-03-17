# Функция для правильного перевода слова во множественное число
def pluralize(word: str) -> str:
    if word in ("data",):
        return word
    elif word.endswith("y") and len(word) > 1 and word[-2] not in "aeiou":
        return word[:-1] + "ies"  # Например, 'city' -> 'cities'
    elif (
        word.endswith("s")
        or word.endswith("x")
        or word.endswith("z")
        or word.endswith("ch")
        or word.endswith("sh")
    ):
        return word + "es"  # Например, 'bus' -> 'buses', 'box' -> 'boxes'
    else:
        return word + "s"  # Например, 'car' -> 'cars'
