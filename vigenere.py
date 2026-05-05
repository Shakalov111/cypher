UA_LOWER = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
UA_UPPER = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
LAT_LOWER = "abcdefghijklmnopqrstuvwxyz"
LAT_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def char_to_key_value(char: str) -> int | None:
    """
    Повертає числове значення символу ключа.
    Підтримує латиницю та кирилицю.
    """
    ch = char.lower()
    if ch in LAT_LOWER:
        return LAT_LOWER.index(ch)
    if ch in UA_LOWER:
        return UA_LOWER.index(ch)
    return None


def build_key_stream(text: str, keyword: str) -> list[int]:
    """
    Будує потік ключів для тексту.
    Пропускає символи, що не входять до алфавіту.
    """
    # Числові значення символів ключового слова
    key_values = []
    for ch in keyword:
        val = char_to_key_value(ch)
        if val is not None:
            key_values.append(val)

    if not key_values:
        raise ValueError("Ключове слово не містить літер.")

    # Розширюємо ключ до довжини тексту (тільки для алфавітних символів)
    stream = []
    key_idx = 0
    for ch in text:
        is_alpha = any(ch in a for a in (UA_LOWER, UA_UPPER, LAT_LOWER, LAT_UPPER))
        if is_alpha:
            stream.append(key_values[key_idx % len(key_values)])
            key_idx += 1
        else:
            stream.append(None)  # не алфавітний символ — ключ не витрачається

    return stream


def process(text: str, keyword: str, decrypt: bool = False) -> str:
    """Шифрування або дешифрування шифром Віженера."""
    key_stream = build_key_stream(text, keyword)
    result = []

    for ch, k in zip(text, key_stream):
        if k is None:
            result.append(ch)
            continue

        direction = -1 if decrypt else 1

        shifted = False
        for alphabet in (UA_LOWER, UA_UPPER, LAT_LOWER, LAT_UPPER):
            if ch in alphabet:
                idx = alphabet.index(ch)
                new_idx = (idx + direction * k) % len(alphabet)
                result.append(alphabet[new_idx])
                shifted = True
                break

        if not shifted:
            result.append(ch)

    return "".join(result)


def encrypt(text: str, keyword: str) -> str:
    return process(text, keyword, decrypt=False)


def decrypt(ciphertext: str, keyword: str) -> str:
    return process(ciphertext, keyword, decrypt=True)


def show_table(text: str, keyword: str):
    """Виводить таблицю шифрування по символах."""
    key_stream = build_key_stream(text, keyword)

    print(f"\n{'Симв.':<7} {'Поз.':<6} {'Ключ-симв.':<12} {'K':<5} {'Результат'}")
    print("-" * 45)

    key_idx = 0
    key_letters = [ch for ch in keyword.lower() if char_to_key_value(ch) is not None]

    for i, (ch, k) in enumerate(zip(text, key_stream)):
        if k is None:
            print(f"  {ch:<5} {i:<6} {'—':<12} {'—':<5} {ch}")
            continue

        key_letter = key_letters[key_idx % len(key_letters)]
        key_idx += 1

        for alphabet in (UA_LOWER, UA_UPPER, LAT_LOWER, LAT_UPPER):
            if ch in alphabet:
                idx = alphabet.index(ch)
                new_idx = (idx + k) % len(alphabet)
                enc_ch = alphabet[new_idx]
                print(f"  {ch:<5} {i:<6} {key_letter:<12} {k:<5} {enc_ch}")
                break


def main():
    print("=" * 50)
    print("  ШИФР ВІЖЕНЕРА")
    print("=" * 50)

    print("\nОберіть дію:")
    print("  1 — Зашифрувати")
    print("  2 — Розшифрувати")
    choice = input("Ваш вибір (1/2): ").strip()

    text = input("Введіть текст: ").strip()
    if not text:
        print("Текст не може бути порожнім.")
        return

    keyword = input("Введіть ключове слово: ").strip()
    if not keyword:
        print("Ключове слово не може бути порожнім.")
        return

    try:
        if choice == "1":
            result = encrypt(text, keyword)
            print(f"\nВідкритий текст : {text}")
            print(f"Ключове слово   : {keyword}")
            print(f"Шифротекст      : {result}")
            show_table(text, keyword)

            check = decrypt(result, keyword)
            print(f"\nПеревірка (розшифровка): {check}")
            print(f"Результат: {'OK' if check == text else 'ПОМИЛКА'}")

        elif choice == "2":
            result = decrypt(text, keyword)
            print(f"\nШифротекст      : {text}")
            print(f"Ключове слово   : {keyword}")
            print(f"Розшифрований   : {result}")

        else:
            print("Невірний вибір.")

    except ValueError as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    main()
