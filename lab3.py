import collections
import os

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
M = 31
M_SQ = M * M
TOP_LANG = ['ст', 'но', 'то', 'на', 'ен']

RARE_BIGRAMS = ["щт","ьо","ыж","юв","яы","аы","бй","гй","дй","еы",
                "шщ","шя","щб","щд","щж","ьы","ыа","ыь","ыы","ыэ"]

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    g, y, x = extended_gcd(b % a, a)
    return g, x - (b // a) * y, y

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1: return None 
    return (x % m + m) % m

def solve_linear_congruence(a, b, m):
    g, x, y = extended_gcd(a, m)
    if b % g != 0: return []
    x0 = (x * (b // g)) % (m // g)
    return [x0 + i * (m // g) for i in range(g)]

def clean_text(text):
    text = text.lower()
    text = text.replace('ё', 'е').replace('ъ', 'ь')
    return "".join([c for c in text if c in ALPHABET])

def bigram_to_int(bg):
    return ALPHABET.index(bg[0]) * M + ALPHABET.index(bg[1])

def int_to_bigram(val):
    first = ALPHABET[val // M]
    second = ALPHABET[val % M]
    return first + second

def get_top_bigrams_from_text(text, n=5):
    bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2) if len(text[i:i+2])==2]
    return [item[0] for item in collections.Counter(bigrams).most_common(n)]

def decrypt_text(ciphertext, a, b):
    a_inv = mod_inverse(a, M_SQ)
    if a_inv is None: return ""
    plaintext = []
    for i in range(0, len(ciphertext)-1, 2):
        bg = ciphertext[i:i+2]
        Y = bigram_to_int(bg)
        X = (a_inv * (Y - b)) % M_SQ
        plaintext.append(int_to_bigram(X))
    return "".join(plaintext)

def score_text(text):
    bgs = [text[i:i+2] for i in range(0, len(text), 2)]
    return sum(bg in RARE_BIGRAMS for bg in bgs)

def main():
    filename = input("Введіть назву файлу: ").strip() or "cipher6.txt"
    
    if not os.path.exists(filename):
        print("Помилка: Файл не знайдено.")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        cipher_clean = clean_text(f.read())
    
    top_cipher = get_top_bigrams_from_text(cipher_clean, 5)
    print(f"\n5 найчастіших біграм шифртексту: {', '.join(top_cipher)}")

    candidates = set()
    for i in range(len(TOP_LANG)):
        for j in range(len(TOP_LANG)):
            if i == j: continue
            X1, X2 = bigram_to_int(TOP_LANG[i]), bigram_to_int(TOP_LANG[j])
            
            for k in range(len(top_cipher)):
                for l in range(len(top_cipher)):
                    if k == l: continue
                    Y1, Y2 = bigram_to_int(top_cipher[k]), bigram_to_int(top_cipher[l])
                    
                    diff_X, diff_Y = (X1 - X2) % M_SQ, (Y1 - Y2) % M_SQ
                    possible_as = solve_linear_congruence(diff_X, diff_Y, M_SQ)
                    
                    for a in possible_as:
                        if extended_gcd(a, M)[0] == 1:
                            b = (Y1 - a * X1) % M_SQ
                            candidates.add((a, b))

    print(f"Знайдено можливих кандидатів на ключ: {len(candidates)}")

    results = []
    for a, b in candidates:
        decrypted = decrypt_text(cipher_clean, a, b)
        if decrypted:
            s = score_text(decrypted)
            results.append((s, decrypted, a, b))

    results.sort(key=lambda x: x[0], reverse=False)

    print("\n--- ТОП-5 ВАРІАНТІВ ---")
    for i in range(min(5, len(results))):
        score, text, a, b = results[i]
        print(f"{i+1}. Ключ ({a}, {b}) [Штраф: {score}]: {text[:60]}...")

    if results:
        best_score, best_text, best_a, best_b = results[0]
        print("\n--- ПОВНИЙ РОЗШИФРОВАНИЙ ТЕКСТ (Найкращий варіант) ---")
        print(f"Ключ: a={best_a}, b={best_b}")
        print("-" * 50)
        print(best_text)
    else:
        print("\nНе вдалося розшифрувати текст.")

if __name__ == "__main__":
    main()