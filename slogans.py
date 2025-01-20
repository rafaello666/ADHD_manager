# slogans.py

import random

SLOGANS = [
    "Rozpieprz chaos i działaj z jajem – Twoje zadania same się nie zrobią!",
    "Twoje życie, Twoje zasady. Zrób to konkretnie albo w ogóle nie zawracaj sobie dupy.",
    "Zamiast pierdolić o marzeniach – wrzuć je w kalendarz i zacznij je realizować.",
    "Bądź jak Brad Pitt: ogarnięty, z klasą i gotowy na każdą akcję. Harmonogram w dłoń!",
    "Masz zadania? To je, kurwa, zrób i przestań szukać wymówek!",
    "Nie chowaj swoich talentów w piwnicy. Postaw je w światło reflektorów i jedź z koksem!",
    "Wyłącz narzekanie, włącz zarządzanie. Czas to Twój atut – nie zmarnuj go."
]

def get_random_slogan():
    return random.choice(SLOGANS)
