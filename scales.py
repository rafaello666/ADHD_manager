# scales.py

"""
Definicje skal (1–10 + 'NIE WIEM') 
dla starych i monikowych kluczy w ADHD Manager ULTRA-ART.
"""

SCALES = {
    "pilne_dla_przetrwania": {
        1:"Brak wpływu", 2:"Minimalny",3:"Mały",4:"Lekki",5:"Średni",
        6:"Dość ważny",7:"Znaczący",8:"Bardzo ważny",9:"Krytyczny",
        10:"Absolutnie kluczowe","NIE WIEM":"Nie wiem"
    },
    "dlugoterminowe_znaczenie": {
        1:"Zero długofal.",2:"Znikomy",3:"Niewielki",4:"Lekki",5:"Średni",
        6:"Dość istotny",7:"Znaczący",8:"Bardzo ważny",9:"Krytyczny",
        10:"Fundamentalny","NIE WIEM":"Niepewny"
    },
    "konsekwencje_opoznienia": {
        1:"Brak skutków",2:"Niewielkie",3:"Mała kara",4:"Średnie trudn.",
        5:"Problematyczne",6:"Poważne",7:"Wielkie straty",8:"B. poważne",
        9:"Krytyczne",10:"Katastrofa","NIE WIEM":"Nie wiadomo"
    },
    "czas_realizacji": {
        1:"B. długo",2:"Raczej długo",3:"Kilka dni",4:"2-3 dni",5:"1 dzień",
        6:"Kilka godzin",7:"~1h",8:"Kilkanaście min",9:"Krótko",10:"Natychmiast",
        "NIE WIEM":"Brak danych"
    },
    "potrzebne_zasoby":{
        1:"Ogromne/kosztowne",2:"Znaczące trudne",3:"Dość kosztowne",4:"Zauważalne",
        5:"Średnie",6:"Dość łatwe",7:"Niewielkie koszty",8:"B. proste",
        9:"Minimalne nakłady",10:"Niepotrzebne", "NIE WIEM":"Niepewne"
    },
    "deadline_strictness":{
        1:"Brak deadline'u",2:"Elastyczny",3:"Raczej luźny",4:"Trochę termin",
        5:"Średni",6:"Ważny termin",7:"Ścisły",8:"B. ścisły",9:"Krytyczny",
        10:"Niedopuszczalny do przekroczenia","NIE WIEM":"Nie wiem"
    },

    "wplyw_na_monike_1h":{
        1:"Brak w 1h",2:"Minimalny 1h",3:"Niewielki 1h",4:"Lekki 1h",5:"Średni 1h",
        6:"Dość ważne 1h",7:"Znaczące 1h",8:"B. źle w 1h",9:"Krytyczne 1h",
        10:"Katastrofa 1h","NIE WIEM":"Nie potrafię ocenić"
    },
    "wplyw_na_monike_3h":{
        1:"Brak w 3h",2:"Minimalny 3h",3:"Niewielki 3h",4:"Lekki 3h",5:"Średni 3h",
        6:"Dość ważne 3h",7:"Znaczące 3h",8:"B. źle w 3h",9:"Krytyczne 3h",
        10:"Katastrofa 3h","NIE WIEM":"Nie wiem"
    },
    "wplyw_na_monike_12h":{
        1:"Brak w 12h",2:"Minimalny 12h",3:"Lekki dyskomfort",4:"Umiarkowany",
        5:"Średni 12h",6:"Dość ważny 12h",7:"Znaczący 12h",8:"B. źle 12h",
        9:"Krytyczne 12h",10:"Katastrofa 12h","NIE WIEM":"Nie wiem"
    },
    "wplyw_na_monike_48h":{
        1:"Brak w 48h",2:"Minimalny",3:"Niewielki",4:"Lekki",5:"Średni",
        6:"Dość ważne 48h",7:"Znaczące 48h",8:"B. źle 48h",9:"Krytyczne 48h",
        10:"Katastrofa 48h","NIE WIEM":"Nie wiem"
    }
}

def get_scale_description(key: str)-> str:
    if key not in SCALES:
        return "Brak zdefiniowanej skali."
    scale_dict = SCALES[key]
    lines = []
    for k,v in scale_dict.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)
