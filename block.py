import math
import os


def get_column_order(keyword: str) -> list[int]:
    """
    Визначає порядок стовпців на основі ключового слова.
    Літера з меншим алфавітним номером отримує менший номер.
    """
    indexed = [(ch.lower(), i) for i, ch in enumerate(keyword)]
    sorted_chars = sorted(indexed, key=lambda x: (x[0], x[1]))
    order = [0] * len(keyword)
    for rank, (_, original_idx) in enumerate(sorted_chars):
        order[original_idx] = rank + 1
    return order


def encrypt_block(block: list[str], col_order: list[int]) -> list[str]:
    """Шифрує один блок — переставляє символи за ключем."""
    key_len = len(col_order)
    result = [''] * key_len
    for new_pos, col_num in enumerate(col_order):
        result[col_num - 1] = block[new_pos] if new_pos < len(block) else ' '
    return result


def decrypt_block(block: list[str], col_order: list[int]) -> list[str]:
    """Дешифрує один блок — повертає символи на початкові місця."""
    key_len = len(col_order)
    result = [''] * key_len
    for new_pos, col_num in enumerate(col_order):
        result[new_pos] = block[col_num - 1] if (col_num - 1) < len(block) else ' '
    return result


def encrypt_text(text: str, keyword: str) -> str:
    """Шифрує весь текст блочною перестановкою."""
    col_order = get_column_order(keyword)
    key_len = len(keyword)

    # Доповнюємо текст пробілами до кратності розміру блоку
    padded = text.ljust(math.ceil(len(text) / key_len) * key_len)

    result = []
    for i in range(0, len(padded), key_len):
        block = list(padded[i:i + key_len])
        encrypted_block = encrypt_block(block, col_order)
        result.extend(encrypted_block)

    return "".join(result)


def decrypt_text(ciphertext: str, keyword: str) -> str:
    """Дешифрує весь текст блочною перестановкою."""
    col_order = get_column_order(keyword)
    key_len = len(keyword)

    result = []
    for i in range(0, len(ciphertext), key_len):
        block = list(ciphertext[i:i + key_len])
        decrypted_block = decrypt_block(block, col_order)
        result.extend(decrypted_block)

    return "".join(result).rstrip()


def read_file(filename: str) -> str:
    """Зчитує текст із файлу."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл '{filename}' не знайдено.")
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filename: str, content: str):
    """Записує текст у файл."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def print_key_info(keyword: str):
    """Виводить інформацію про ключ."""
    col_order = get_column_order(keyword)
    print(f"\n  Ключове слово  : {keyword}")
    print(f"  Довжина блоку  : {len(keyword)} символів")
    print(f"  Порядок стовпців: {col_order}")
    print(f"  Візуалізація ключа:")
    print(f"    Позиція : " + " ".join(f"{i+1:>3}" for i in range(len(keyword))))
    print(f"    Літера  : " + " ".join(f"{ch:>3}" for ch in keyword.lower()))
    print(f"    Номер   : " + " ".join(f"{n:>3}" for n in col_order))


def main():
    print("=" * 55)
    print("  КЛЮЧОВИЙ БЛОЧНИЙ ШИФР ПЕРЕСТАНОВКИ")
    print("=" * 55)

    print("\nОберіть дію:")
    print("  1 — Зашифрувати текст із файлу")
    print("  2 — Розшифрувати текст із файлу")
    choice = input("Ваш вибір (1/2): ").strip()

    if choice not in ("1", "2"):
        print("Невірний вибір.")
        return

    input_file = input("Введіть назву вхідного файлу (наприклад, text.txt): ").strip()
    if not input_file.endswith(".txt"):
        input_file += ".txt"

    try:
        text = read_file(input_file)
    except FileNotFoundError as e:
        print(f"\nПомилка: {e}")
        return

    keyword = input("Введіть ключове слово: ").strip()
    if not keyword:
        print("Ключове слово не може бути порожнім.")
        return

    print_key_info(keyword)

    if choice == "1":
        output_file = input("\nВведіть назву файлу для шифротексту (наприклад, encrypted.txt): ").strip()
        if not output_file.endswith(".txt"):
            output_file += ".txt"

        result = encrypt_text(text, keyword)
        write_file(output_file, result)

        print(f"\n  Вхідний файл   : {input_file}")
        print(f"  Вихідний файл  : {output_file}")
        print(f"  Символів у тексті    : {len(text)}")
        print(f"  Кількість блоків     : {math.ceil(len(text) / len(keyword))}")
        print(f"  Символів у шифртексті: {len(result)}")
        print(f"\n  Перші 80 символів шифртексту:")
        print(f"  {result[:80]}...")
        print(f"\n  Файл '{output_file}' збережено.")

    elif choice == "2":
        output_file = input("\nВведіть назву файлу для розшифрованого тексту (наприклад, decrypted.txt): ").strip()
        if not output_file.endswith(".txt"):
            output_file += ".txt"

        result = decrypt_text(text, keyword)
        write_file(output_file, result)

        print(f"\n  Вхідний файл   : {input_file}")
        print(f"  Вихідний файл  : {output_file}")
        print(f"  Символів у шифртексті  : {len(text)}")
        print(f"  Символів після розшифровки: {len(result)}")
        print(f"\n  Перші 80 символів розшифрованого тексту:")
        print(f"  {result[:80]}...")
        print(f"\n  Файл '{output_file}' збережено.")


if __name__ == "__main__":
    main()