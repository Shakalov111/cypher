import math

UA_ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"


def get_column_order(keyword: str) -> list[int]:
    """
    Визначає порядок стовпців на основі ключового слова.
    Літера з меншим алфавітним номером отримує менший номер стовпця.
    """
    keyword_lower = keyword.lower()
    indexed = [(char, i) for i, char in enumerate(keyword_lower)]
    sorted_chars = sorted(indexed, key=lambda x: UA_ALPHABET.index(x[0]) if x[0] in UA_ALPHABET else ord(x[0]))
    order = [0] * len(keyword_lower)
    for rank, (_, original_idx) in enumerate(sorted_chars):
        order[original_idx] = rank + 1
    return order


def clean_text(text: str) -> str:
    """Видаляє неалфавітні символи та переводить у нижній регістр."""
    return "".join(ch for ch in text.lower() if ch in UA_ALPHABET)


def encrypt(text: str, keyword: str) -> str:
    """
    Шифрування методом вертикальної перестановки.
    """
    cleaned = clean_text(text)
    key_len = len(keyword)
    col_order = get_column_order(keyword)

    # Заповнення таблиці (рядками)
    num_rows = math.ceil(len(cleaned) / key_len)
    padded = cleaned.ljust(num_rows * key_len, "х")  # доповнення символом 'х'

    table = []
    for i in range(num_rows):
        table.append(list(padded[i * key_len:(i + 1) * key_len]))

    # Зчитування по стовпцях у порядку нумерації
    ciphertext = ""
    for col_num in range(1, key_len + 1):
        col_idx = col_order.index(col_num)
        for row in table:
            ciphertext += row[col_idx]

    return ciphertext


def decrypt(ciphertext: str, keyword: str) -> str:
    """
    Дешифрування методом вертикальної перестановки.
    """
    key_len = len(keyword)
    col_order = get_column_order(keyword)
    num_rows = math.ceil(len(ciphertext) / key_len)

    # Визначаємо довжину кожного стовпця
    col_lengths = [num_rows] * key_len

    # Зчитуємо стовпці у порядку нумерації та відновлюємо таблицю
    table = [[""] * key_len for _ in range(num_rows)]
    pos = 0
    for col_num in range(1, key_len + 1):
        col_idx = col_order.index(col_num)
        for row in range(col_lengths[col_idx]):
            table[row][col_idx] = ciphertext[pos]
            pos += 1

    # Зчитування по рядках
    plaintext = ""
    for row in table:
        plaintext += "".join(row)

    return plaintext


def print_table(text: str, keyword: str, label: str = "Таблиця"):
    """Виводить таблицю шифрування у зручному форматі."""
    cleaned = clean_text(text)
    key_len = len(keyword)
    col_order = get_column_order(keyword)
    num_rows = math.ceil(len(cleaned) / key_len)
    padded = cleaned.ljust(num_rows * key_len, "х")

    print(f"\n{label}:")
    header = " | ".join(f"{ch:^3}" for ch in keyword.lower())
    order_row = " | ".join(f"{col_order[i]:^3}" for i in range(key_len))
    sep = "-" * (key_len * 6 - 1)

    print(f"  {header}")
    print(f"  {order_row}")
    print(f"  {sep}")
    for i in range(num_rows):
        row = padded[i * key_len:(i + 1) * key_len]
        print("  " + " | ".join(f"{ch:^3}" for ch in row))


def main():
    
    print("\nОберіть дію:")
    print("  1 — Зашифрувати текст")
    print("  2 — Розшифрувати текст")
    choice = input("Ваш вибір (1/2): ").strip()

    keyword = input("Введіть ключове слово (гасло): ").strip()
    if not keyword:
        print("Ключове слово не може бути порожнім.")
        return

    col_order = get_column_order(keyword)
    print(f"\nКлючове слово : {keyword.lower()}")
    print(f"Порядок стовпців: {col_order}")

    if choice == "1":
        text = input("Введіть відкритий текст: ").strip()
        if not text:
            print("Текст не може бути порожнім.")
            return

        cleaned = clean_text(text)
        print(f"Очищений текст: {cleaned}")
        print_table(text, keyword, "Таблиця шифрування")

        result = encrypt(text, keyword)
        print(f"\nШифротекст: {result}")

        # Групи по 5 символів
        groups = " ".join(result[i:i+5] for i in range(0, len(result), 5))
        print(f"Шифротекст (групи по 5): {groups}")

    elif choice == "2":
        ciphertext = input("Введіть шифротекст: ").strip().replace(" ", "")
        result = decrypt(ciphertext, keyword)
        print(f"\nРозшифрований текст: {result}")

    else:
        print("Невірний вибір.")


if __name__ == "__main__":
    main()