# Užduoties vykdymas:

1. Užduočių sąrašas
1. Užduoties tipo ir ID gavimas
2. Užduoties pradėjimas
3. Užduoties atlikimas

## Užduočių informacija

Visų užduočių sąrašas su pagrindine informacija (bet ne specifine) yra čia:

http://rainbowchallenge.lt/api/challenge/

Užduotis identifikuojama pagal lauką `uuid`

## Užduoties pradėjimas

Vartotojui pasirinkus užduotį, turi būti sukuriamas objektas POST metodu į atitinkamos užduoties endpoint'ą:

### Straipsnio rašymo užduotis

Jei tipas yra "article":
http://127.0.0.1:8000/api/article_joined_challenge/

Turi būti siunčiami šie duomenys:

```json
{
    "main_joined_challenge": {
        "status": null,
        "user": null,
        "challenge": null
    },
    "article_name": "",
    "article_url": ""
}
```

Būtini duomenys: 
status - `joined`
user - vartotojo `uuid`
challenge - užduoties `uuid`

### Dalyvavimas renginyje

Jei tipas yra "event":
http://127.0.0.1:8000/api/article_joined_challenge/

Turi būti siunčiami šie duomenys:

```json
{
        "main_joined_challenge": {
            "status": "joined",
            "user": "11771309-f657-4ef6-a2bd-0fa6d1a95b28",
            "challenge": "cbed2257-98f4-4be3-a894-66f05600db25"
        }
    }
```

Būtini duomenys: 
status - `joined`
user - vartotojo `uuid`
challenge - užduoties `uuid`

## Užduoties atlikimas

TBC