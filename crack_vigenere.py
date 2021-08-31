#!/usr/bin/python3

import re

ENGLISH_LETTERS_FREQUENCY = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

FRENCH_LETTERS_FREQUENCY_ACCENTS = {'E': 15.10, 'A': 8.13, 'S': 7.91, 'T': 7.11, 'I': 6.94, 'R': 6.43, 'N': 6.42, 'U': 6.05, 'L': 5.68, 'O': 5.27, 'D': 3.55, 'M': 3.23, 'C': 3.15, 'P': 3.03, 'É': 2.13, 'V': 1.83, 'H': 1.08, 'G': 0.97, 'F': 0.96, 'B': 0.93, 'Q': 0.89, 'J': 0.71, 'À': 0.54, 'X': 0.42, 'È': 0.35, 'Ê': 0.24, 'Z': 0.21, 'Y': 0.19, 'K': 0.16, 'Ô': 0.07, 'Û': 0.05, 'W': 0.04, 'Â': 0.03, 'Î': 0.03, 'Ü': 0.02, 'Ù': 0.02, 'Ë': 0.01, 'Œ': 0.01, 'Ç': 0.008, 'Ï': 0.008 }
#FRENCH_ACCENTS = {'E': ['É', 'È', 'Ê', 'Ë', 'Œ'], 'O': ['Ô'], 'U': ['Û', 'Ü', 'Ù'], 'I': ['Î', 'Ï'], 'A': ['Â', 'À'], 'C': ['Ç']}
FRENCH_ACCENTS = {'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E', 'Œ': 'E', 'Ô': 'O', 'Û': 'U', 'Ü': 'U', 'Ù': 'U', 'Î': 'I', 'Ï': 'I', 'Â': 'A', 'À': 'A', 'Ç': 'C'}
FRENCH_LETTERS_FREQUENCY = {}

for letter in FRENCH_LETTERS_FREQUENCY_ACCENTS:
    if letter in FRENCH_ACCENTS:
        mainLetter = FRENCH_ACCENTS[letter] # Letter without accent
        if mainLetter not in FRENCH_LETTERS_FREQUENCY:
            FRENCH_LETTERS_FREQUENCY[mainLetter] = 0
        FRENCH_LETTERS_FREQUENCY[mainLetter] += FRENCH_LETTERS_FREQUENCY_ACCENTS[letter]
    else:
        if letter not in FRENCH_LETTERS_FREQUENCY:
            FRENCH_LETTERS_FREQUENCY[letter] = 0
        FRENCH_LETTERS_FREQUENCY[letter] += FRENCH_LETTERS_FREQUENCY_ACCENTS[letter]

#print(FRENCH_LETTERS_FREQUENCY)

formatted = open('formatted.txt', 'r').read()

# Diviser le texte en parties de la taille de la clé
key_length = 9
chunks = re.findall(".{%s}|.+" % key_length , formatted)

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Applique un décalage de key sur char dans la direction shift_direction
def vigenere_shift(char, key, shift_direction=-1):
    key_index = LETTERS.find(key.upper())
    char_index = LETTERS.find(char)

    char_index += key_index * shift_direction
    char_index %= len(LETTERS)

    return LETTERS[char_index]

# parts correspond aux parties du texte de taille len(key), key au caractère de la potentielle clé et index à
# l'index du caractère de chaque part sur lequel appliquer le décalage et effectuer l'analyse de fréquence
# Retourne : dict[str, int] avec str correspondant au caractère et int son nombre d'apparition,
# par exemple {'E': 10, 'A': 6}
def freq_count(parts: list[str], key_char: str, index: int) -> dict[str, int]:
    counts = {}
    for part in parts:
        if len(part) > index:
            part_char = part[index]
            result_char = vigenere_shift(part_char, key_char)
            if result_char not in counts:
                counts[result_char] = 0
            counts[result_char] += 1
    return counts

# Calculer la probabilité globale par rapport à une liste de fréquences
# Sur 5 caractères, si on a 2 fois la lettre E et une fois la lettre A, il y a plus de probabilités que ça
# corresponde à la langue car plus proche de plutôt que FRENCH_LETTERS_FREQUENCY que d'une chaîne de 5
# caractères rares comme V, J, Q, Z...
# Mais il ne faut pas que les lettres qui apparaissent le plus souvent compte tous le temps plus, car si on
# a beaucoup trop de E alors ce n'est pas bon non plus
# Je vais tenter un calcul qui est la somme de chaque lettre rencontrées multiplié par sa probabilité d'apparition
# et le nombre de fois qu'elle apparaît, le total devrait se rapprocher le plus possible de 100 pour 26 caractères,
# donc le score moyen de chaque lettre devrait être de 100/26 soit environ 3.85
# Je remarque que chaque lettre de la clé finale "THEMENTOR" ressort largement par rapport aux autres avec un score
# largement supérieur au reste, mais aussi bien au-dessus de la moyenne calculée
# La faille avec ma méthode c'est que les lettres ne sont plus considérées que comme des nombres et donc deux
# lettres avec une fréquence proche (comme R et N) sont confondues : NR, RR et RN donneront le même score
def probability_score_v1(freq: dict[str, int]):
    # 100 car la somme de toutes les valeurs de FRENCH_LETTERS_FREQUENCY doit valoir 100
    # 26 car c'est le nombre de valeurs de FRENCH_LETTERS_FREQUENCY (lettres dans l'alphabet)
    IDEAL_AVERAGE_PER_LETTER = 100 / 26
    prob_sum = 0
    letters_count = 0
    for letter, count in freq.items():
        frequency = FRENCH_LETTERS_FREQUENCY[letter]
        prob_sum += (frequency * count)
        letters_count += count
    print("{} / {} ({} letters)".format(prob_sum, IDEAL_AVERAGE_PER_LETTER * letters_count, letters_count))

# Une autre idée est de calculée combien de fois chaque lettre devrait apparaître en se basant sur le nombre
# de lettres au total et leur probabilités d'apparaître
def probability_score_v2(freq: dict[str, int]):
    letters_count = sum(freq.values()) # Nombre total de lettres
    all_differences = {} # Stocker toutes les différences, je garde les lettres en index au cas où

    for letter, count in freq.items():
        # Par exemple, si la lettre E apparaît à une fréquence de 18% et qu'on a 20 lettres
        # E devrait apparaître 18 / 100 * letters_count = 3.6 fois
        target_frequency = round(FRENCH_LETTERS_FREQUENCY[letter] / 100 * letters_count, 2)
        # Fréquence d'apparition dans le texte
        actual_frequency = count
        # On stocke la différence de fréquence
        all_differences[letter] = abs(target_frequency - actual_frequency)
        #print("La lettre {} devrait apparaitre {} fois mais apparait {} fois".format(letter, target_frequency, actual_frequency))

    # Calcul de la moyenne de différence de fréquence pour les lettres, le but est d'être le plus proche possible de 0
    difference_average = sum(all_differences.values()) / len(all_differences)
    # Une amélioration possible serait de prendre en compte la probabilité de chaque lettre
    # Par exemple, si on a 3 lettres Y au lieu de 0.5, l'écart devrait avoir un poids plus important puisque la lettre
    # Y a une fréquence faible. En même temps, la fréquence de chaque lettre sert déjà à déterminer le nombre de fois
    # qu'elle devrait apparaître, par exemple 3 lettres Y au lieu de 0.5 correspond à 60 lettres E au lieu de 10
    # Le coefficient ici est le même : X6, et devrait avoir le même impact alors qu'ici l'impact est de 2.5 pour Y
    # et 50 pour E, il faudrait calculer le ratio au lieu de la différence je pense
    #print(difference_average)
    return difference_average

# Calcul de la clé la plus probable à l'aide de l'analyse de fréquence
for key_index in range(0, key_length):
    best_score = [ "", None ] # [0] -> letter, [1] -> score

    for letter in LETTERS:
        freq = freq_count(chunks, letter, key_index)
        score = probability_score_v2(freq)
        if best_score[1] is None or score < best_score[1]:
            best_score = [ letter, score ]

    print("Meilleur score : {} pour key[{}] = {}".format(best_score[1], key_index, best_score[0]))
