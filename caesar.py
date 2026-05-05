UA_LOWER = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
UA_UPPER = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
LAT_LOWER = "abcdefghijklmnopqrstuvwxyz"
LAT_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def shift_char(char: str, key: int, decrypt: bool = False) -> str:
    """Зсуває один символ на key позицій."""
    direction = -1 if decrypt else 1

    for alphabet in (UA_LOWER, UA_UPPER, LAT_LOWER, LAT_UPPER):
        if char in alphabet:
            idx = alphabet.index(char)
            new_idx = (idx + direction * key) % len(alphabet)
            return alphabet[new_idx]

    return char  # символ не в алфавіті — повертаємо без змін


def encrypt(text: str, key: int) -> str:
    """Шифрування тексту шифром Цезаря."""
    return "".join(shift_char(ch, key) for ch in text)


def decrypt(ciphertext: str, key: int) -> str:
    """Дешифрування тексту шифром Цезаря."""
    return "".join(shift_char(ch, key, decrypt=True) for ch in ciphertext)


def show_table(text: str, key: int):
    """Виводить таблицю відповідності символів."""
    print(f"\n{'Символ':<10} {'Номер':<8} {'Зсув':<8} {'Зашифр.':<10}")
    print("-" * 38)
    for ch in text:
        for alphabet in (UA_LOWER, UA_UPPER, LAT_LOWER, LAT_UPPER):
            if ch in alphabet:
                idx = alphabet.index(ch)
                new_idx = (idx + key) % len(alphabet)
                print(f"  {ch:<8} {idx:<8} {new_idx:<8} {alphabet[new_idx]:<10}")
                break
        else:
            print(f"  {ch:<8} {'—':<8} {'—':<8} {ch:<10}")


def main():
    print("=" * 50)
    print("  ШИФР ЦЕЗАРЯ")
    print("=" * 50)

    print("\nОберіть дію:")
    print("  1 — Зашифрувати")
    print("  2 — Розшифрувати")
    choice = input("Ваш вибір (1/2): ").strip()

    text = input("Введіть текст: ").strip()
    if not text:
        print("Текст не може бути порожнім.")
        return

    try:
        key = int(input("Введіть ключ (ціле число): ").strip())
    except ValueError:
        print("Ключ має бути цілим числом.")
        return

    if choice == "1":
        result = encrypt(text, key)
        print(f"\nВідкритий текст : {text}")
        print(f"Ключ            : {key}")
        print(f"Шифротекст      : {result}")
        show_table(text, key)

        # Перевірка
        check = decrypt(result, key)
        print(f"\nПеревірка (розшифровка): {check}")
        print(f"Результат: {'OK' if check == text else 'ПОМИЛКА'}")

    elif choice == "2":
        result = decrypt(text, key)
        print(f"\nШифротекст      : {text}")
        print(f"Ключ            : {key}")
        print(f"Розшифрований   : {result}")

    else:
        print("Невірний вибір.")


if __name__ == "__main__":
    main()