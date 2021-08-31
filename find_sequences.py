#!/usr/bin/python3

import re

text = open("texte.txt", "r").read()

filtered = re.sub(r"[^A-Za-z]+", "", text)
formatted = filtered.upper()

open("formatted.txt", "w").write(formatted)

sequences_length = 9

# Avec seq_len = 3 et pour la chaîne "MOITEPOIT" :
# Les séquences sont : [ "MOI", "OIT", "ITE", "TEP", "EPO", "POI", "OIT" ]
# Le retour devrait être : {'MOI': [0], 'OIT': [1, 6], 'ITE': [2], 'TEP': [3], 'EPO': [4], 'POI': [5]}
def map_sequences(seq_len, text):
    sequences = {}
    for text_pos in range(0, len(text) - seq_len + 1):
        seq = ""
        # Pas opti, splice ?
        for seq_pos in range(0, seq_len):
            seq += text[text_pos + seq_pos]
        if not seq in sequences:
            sequences[seq] = []
        sequences[seq].append(text_pos)
    return sequences

sequences = map_sequences(sequences_length, formatted)
#print(sequences)
# Ensuite, trier pour ne travailler qu'avec les séquences présentes au moins 2 fois

# Dictionnary comprehension
# https://www.datacamp.com/community/tutorials/python-dictionary-comprehension
# dict_variable = {key:value for (key,value) in dictonary.items()}

# Pour me simplifier la vie, je ne garde que les séquences présentes exactement 2 fois dans le texte
sequences_filtered = { seq: positions for (seq, positions) in sequences.items() if len(positions) == 2 }
# Avec sequences_length = 10, on obtient :
# {'LOKTUIEKBL': [168, 1032], 'OKTUIEKBLG': [169, 1033], 'KTUIEKBLGV': [170, 1034], 'TUIEKBLGVL': [171, 1035], 'UIEKBLGVLA': [172, 1036], 'IEKBLGVLAS': [173, 1037], 'EKBLGVLASG': [174, 1038], 'EBWEDGRJIZ': [944, 980], 'BWEDGRJIZE': [945, 981]}
# Avec 10 caractères à la suite, il ne fait aucune doute qu'il s'agit à l'origine du même mot et que la taille de la clé
# est devinable ici. Par exemple, la taille de la clé est probablement un diviseur de (980 - 944 = 36) et de (1033 - 169 = 864)

# Obtenir tous les diviseurs d'un nombre entier
# Il existe des manières plus optimisées, mais c'est la plus simple
def get_divisors(n):
    divisors = []
    for i in range(1, int(n / 2) + 1):
        if n % i == 0:
            divisors.append(i)
    divisors.append(n)
    return divisors

# Calcul de tous les diviseurs possibles pour chaque différence d'une séquence à l'autre
def get_divisors_of_sequences(sequences):
    # key: sequence -> string, value: divisors -> list(int)
    divisors = {}
    for seq in sequences:
        positions = sequences[seq]
        difference = abs(positions[0] - positions[1])
        divisors[seq] = get_divisors(difference)
    return divisors

divisors = get_divisors_of_sequences(sequences_filtered)

# Compter le nombre de fois que chaque diviseur revient pour toutes les séquences
def count_divisors(divisors):
    count = {}
    for seq in divisors:
        seq_divisors = divisors[seq]
        for divisor in seq_divisors:
            if not divisor in count:
                count[divisor] = 0
            count[divisor] += 1
    return count

divisors_count = count_divisors(divisors)

# Ordonner la sortie pour avoir les diviseurs du plus commun au moins commun
# https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
# Depuis Python 3.6, l'ordre dans un dictionnaire est conservé
ordonned = dict(sorted(divisors_count.items(), key=lambda item: item[1], reverse=True))

top_10 = list(ordonned.items())[:10]

# [(1, 55), (3, 55), (9, 55), (2, 31), (6, 31), (18, 31), (4, 25), (12, 25), (36, 25), (27, 24)]
print(top_10)
# On voit que les diviseurs 1, 3 et 9 reviennent 55 fois, ce qui est logique puisque si un nombre
# est divisible par 9 alors il l'est aussi par 3 et 1. Sachant que n'importe quel nombre est divisible
# par 1, le fait qu'il y ait autant de diviseurs par 1 que par 9 montre qu'une taille de clé 9 semble
# être la bonne taille, car 3 serait trop faible et donc moins probablement choisi.


print(sequences_filtered)