import re
import math
from collections import Counter
with open("crypto_lab1.txt", "r", encoding="utf-8") as f:
    text = f.read()
text = text.lower()

text_with_spaces = re.sub(r"[^а-яё\s]", " ", text)
text_with_spaces = re.sub(r"\s+", " ", text_with_spaces).strip()

text_no_spaces = re.sub(r"\s+", "", text_with_spaces)

print("Початок тексту із пробілами:\n", text_with_spaces[:400])
print("\nПочаток тексту без пробілів:\n", text_no_spaces[:400])
print("\nДовжина тексту з пробілами:", len(text_with_spaces))
print("Довжина тексту без пробілів:", len(text_no_spaces))

def chastota_bukv(text):
    counts = Counter(text)
    total = sum(counts.values())
    return {ch: counts[ch] / total for ch in counts}, counts, total

letter_freq_with, letter_counts_with, total_with = chastota_bukv(text_with_spaces)
letter_freq_no, letter_counts_no, total_no = chastota_bukv(text_no_spaces)

print("\nЧастота букв для тексту з пробілами)")
for ch, cnt in letter_counts_with.most_common(33):
    print(f"{ch}: {cnt} ({letter_freq_with[ch]:.5f})")

print("\nЧастота букв для тексту без пробілів")
for ch, cnt in letter_counts_no.most_common(32):
    print(f"{ch}: {cnt} ({letter_freq_no[ch]:.5f})")


def bigrams_count_func(text, step=1):
    bigrams = Counter()
    for i in range(0, len(text) - 1, step):
        pair = text[i:i+2]
        if len(pair) == 2:
            bigrams[pair] += 1
    return bigrams


bigrams_with_overlap = bigrams_count_func(text_with_spaces, step=1)
bigrams_with_nonoverlap = bigrams_count_func(text_with_spaces, step=2)
bigrams_no_overlap = bigrams_count_func(text_no_spaces, step=1)
bigrams_no_nonoverlap = bigrams_count_func(text_no_spaces, step=2)

def bigram_chastota(counter):
    total = sum(counter.values())
    return {bg: counter[bg] / total for bg in counter}, total

bigrams_freq_with_overlap, total_with_overlap = bigram_chastota(bigrams_with_overlap)
bigrams_freq_no_overlap, total_no_overlap = bigram_chastota(bigrams_no_overlap)

print("\n30 найчастіших біграм що перетинаються(текст з пробілами)")
for bg, cnt in bigrams_with_overlap.most_common(30):
    print(f"{bg}: {cnt} ({bigrams_freq_with_overlap[bg]:.6f})")

print("\n30 найчастіших біграм що неперетинаються(текст з пробілами)")
for bg, cnt in bigrams_with_nonoverlap.most_common(30):
    freq = cnt / sum(bigrams_with_nonoverlap.values())
    print(f"{bg}: {cnt} ({freq:.6f})")

print("\n30 найчастіших біграм що перетинаються(текст без пробілів)")
for bg, cnt in bigrams_no_overlap.most_common(30):
    print(f"{bg}: {cnt} ({bigrams_freq_no_overlap[bg]:.6f})")

print("\n30 біграм що неперетинаються(текст без пробілів)")
for bg, cnt in bigrams_no_nonoverlap.most_common(30):
    freq = cnt / sum(bigrams_no_nonoverlap.values())
    print(f"{bg}: {cnt} ({freq:.6f})")

def entropy_H1(text):
    counts = Counter(text)
    total = sum(counts.values())
    H = 0.0
    for c in counts:
        p = counts[c] / total
        H -= p * math.log2(p)
    return H

def entropy_H2(counter):
    total = sum(counter.values())
    H = 0.0
    for count in counter.values():
        p = count / total
        H -= p * math.log2(p)
    return H / 2

H1_with = entropy_H1(text_with_spaces)
H1_no = entropy_H1(text_no_spaces)

H2_with_overlap = entropy_H2(bigrams_with_overlap)
H2_with_nonoverlap = entropy_H2(bigrams_with_nonoverlap)
H2_no_overlap = entropy_H2(bigrams_no_overlap)
H2_no_nonoverlap = entropy_H2(bigrams_no_nonoverlap)

print("\nH1 (з пробілами):", round(H1_with, 6))
print("H1 (без пробілів):", round(H1_no, 6))
print("H2 (з пробілами, перетинаються):", round(H2_with_overlap, 6))
print("H2 (з пробілами, неперетинаються):", round(H2_with_nonoverlap, 6))
print("H2 (без пробілів, перетинаються):", round(H2_no_overlap, 6))
print("H2 (без пробілів, неперетинаються):", round(H2_no_nonoverlap, 6))

import csv

def save_bigrams(counter, total, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Біграма", "Кількість", "Частота"])
        for bg, cnt in counter.most_common():
            freq = cnt / total
            writer.writerow([bg, cnt, f"{freq:.8f}"])

save_bigrams(bigrams_with_overlap, total_with_overlap, "bigrams_with_overlap.csv")
save_bigrams(bigrams_with_nonoverlap, sum(bigrams_with_nonoverlap.values()), "bigrams_with_nonoverlap.csv")
save_bigrams(bigrams_no_overlap, total_no_overlap, "bigrams_no_overlap.csv")
save_bigrams(bigrams_no_nonoverlap, sum(bigrams_no_nonoverlap.values()), "bigrams_no_nonoverlap.csv")