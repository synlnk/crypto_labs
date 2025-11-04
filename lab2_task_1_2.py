import collections
import matplotlib.pyplot as plt
alphabet = list("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя")
m = len(alphabet)
char_to_index = {ch: i for i, ch in enumerate(alphabet)}
index_to_char = {i: ch for i, ch in enumerate(alphabet)}

keys = {
    2: "ок",
    3: "сон",
    4: "лаба",
    5: "клава",
    10: "шифротекст",
    11: "абракадабра",
    12: "криптографія",
    13: "паралелепіпед",
    14: "електростанція",
    15: "перстеньнесефро",
    16: "раздватричотирип",
    17: "омайгадвотіздуінг",
    18: "просторандомнийтек",
    19: "технолоджиявоувоуво",
    20: "ліонелямессіроналдуу"
}
with open("input_text.txt", "r", encoding="utf-8") as f:
    text = f.read().lower()

clean_text = "".join(ch for ch in text if ch in alphabet)

print("=== вихідний текст ===")
print(clean_text)

ic_values_for_plot = []
labels_for_plot = []

def calculate_ic(text):
    n = len(text)
    
    counts = collections.Counter(text)
    
    numerator = sum(n_t * (n_t - 1) for n_t in counts.values())
    
    denominator = n * (n - 1)
    
    return numerator / denominator

ic_plaintext = calculate_ic(clean_text)
print("====")
print(f"Індекс відповідності (відкритий текст): {ic_plaintext:.6f}")
print("====\n")

ic_values_for_plot.append(ic_plaintext)
labels_for_plot.append("Відкритий\nтекст")

def vigenere_encrypt(plaintext, key):
    ciphertext = []
    key_len = len(key)
    for i, ch in enumerate(plaintext):
        p = char_to_index[ch]
        k = char_to_index[key[i % key_len]]
        c = (p + k) % m
        ciphertext.append(index_to_char[c])
    return "".join(ciphertext)

for r, key in keys.items():
    cipher = vigenere_encrypt(clean_text, key)
    
    print(f"=== r={r}, ключ='{key}' ===")
    print(cipher)
    
    ic_cipher = calculate_ic(cipher)
    print("====")
    print(f"Індекс відповідності (шифротекст r={r}): {ic_cipher:.6f}")
    print("====\n")
    
    ic_values_for_plot.append(ic_cipher)
    labels_for_plot.append(f"r={r}")

bar_colors = ['green'] + ['blue'] * (len(labels_for_plot) - 1) 

plt.figure(figsize=(15, 7)) 

plt.bar(labels_for_plot, ic_values_for_plot, color=bar_colors)

plt.title("Порівняння IC відкритого тексту та шифртекстів")
plt.xlabel("Тип тексту (r = довжина ключа)")
plt.ylabel("Індекс відповідності (IC)")

plt.show()