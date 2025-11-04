import collections

alphabet = list("абвгдежзийклмнопрстуфхцчшщъыьэюя")
m = len(alphabet)
char_to_index = {ch: i for i, ch in enumerate(alphabet)}
index_to_char = {i: ch for i, ch in enumerate(alphabet)}

with open("cypher.txt", "r", encoding="utf-8") as f:
    file_content = f.read()
    ciphertext = "".join(ch for ch in file_content if ch in alphabet)

def calculate_ic(text):
    n = len(text)
    counts = collections.Counter(text)
    numerator = sum(n_t * (n_t - 1) for n_t in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator


for r in range(2, 31):
    columns = [""] * r
    for i, char in enumerate(ciphertext):
        columns[i % r] += char
        
    ics_for_this_r = [calculate_ic(col_text) for col_text in columns if len(col_text) >= 2]
    
    if ics_for_this_r:
        avg_ic = sum(ics_for_this_r) / len(ics_for_this_r)
    else:
        avg_ic = 0.0
        
    print(f"r = {r:2}: Середній IC = {avg_ic:.6f}")


R = 15
print("Аналіз блоків для r = 15")

blocks = [""] * R
for i, ch in enumerate(ciphertext):
    blocks[i % R] += ch

most_common_letters_per_block = []


for i, block in enumerate(blocks):
    counter = collections.Counter(block)
    most_common = counter.most_common(4)
    print(f"\n--- Блок {i} ---")
    print(f"Довжина блоку: {len(block)}")
    print(f"Найчастіші літери: {most_common}")
    most_common_letters_per_block.append(most_common[0][0])


TARGET_CHARS_GUESS = {
    'о': char_to_index['о'],
    'е': char_to_index['е'],
    'а': char_to_index['а']
}
found_keys = {}

for guess_char, guess_index in TARGET_CHARS_GUESS.items():
    current_key_chars = []
    for i in range(R):
        most_common_char = most_common_letters_per_block[i]
        c_index = char_to_index[most_common_char]
        k_index = (c_index - guess_index + m) % m
        k_char = index_to_char[k_index]
        current_key_chars.append(k_char)
        
    found_keys[guess_char] = "".join(current_key_chars)

print(f"\nКлюч (припущення: 'о'): {found_keys['о']}")
print(f"Ключ (припущення: 'е'): {found_keys['е']}")
print(f"Ключ (припущення: 'а'): {found_keys['а']}")


def vigenere_decrypt(text_to_decrypt, key):
    plaintext = []
    key_len = len(key)
    for i, ch in enumerate(text_to_decrypt):
        c = char_to_index[ch]
        k = char_to_index[key[i % key_len]]
        p = (c - k + m) % m 
        plaintext.append(index_to_char[p])
    return "".join(plaintext)

print("\nДешифрування ключем 'абсолютныйигрок'")

FINAL_KEY_GUESS = "абсолютныйигрок"
decrypted_text_guess = vigenere_decrypt(ciphertext, FINAL_KEY_GUESS)

print(decrypted_text_guess) 