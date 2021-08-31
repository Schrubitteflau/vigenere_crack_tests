#!/usr/bin/python3

import math

text = open("texte.txt", "r").read()

# Suppression de certains caractères
text = text.replace("\n", " ").replace(".", "").replace(",", "").replace(":", "").replace("\"", "").replace("'", "").lower()

out = open("formatted.txt", "w")
out.write(text)

# key: word, value: array of positions
positions = {}
pos_count = 0

words = text.split()

# Ajout des positions
for word in words:
    if not word in positions:
        positions[word] = []
    positions[word].append(pos_count)
    pos_count += len(word)

# key: word, value: array of differences
differences = {}

# Calcul des différences pour tous les mots dont on a trouvé au moins 2 occurences
# Résultat attendu pour :
# positions = { "ahij": [1562, 1859, 2021, 2255] }
# differences = { "ahij": [234, 162, 297]}
# Car : (2255 - 2021 = 234), puis (2021 - 1859 = 162), puis (1859 - 1562 = 297)
for word in positions:
    pos = positions[word]
    nPos = len(pos)

    # Si 2 entrées, alors [1] - [0]
    # Sinon, on ajoute les différences pos[n] - pos[n - 1] jusqu'à ce que n - 1 = 0
    if nPos > 1:
        differences[word] = []
        # range() stop is exclusive, so it will never reach 0 but stop at 1
        for i in range(nPos - 1, 0, -1):
            differences[word].append(pos[i] - pos[i - 1])


gdcs = {}

# Ensuite, on va chercher le PGCD commun à tous les nombres, mais il peut y avoir de faux positifs : mots identiques après
# chiffrement mais pas dans le texte en clair.
# Pour me simplifier la tâche je vais calculer le PGCD commun pour tous les mots ayant été trouvés au moins 3 fois
for word in differences:
    diff = differences[word]

    if len(diff) > 1:
        gdcs[word] = math.gcd(*diff)

print(gdcs)
