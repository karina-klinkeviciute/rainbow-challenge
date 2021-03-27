Užduoties vykdymas:

1. Užduočių sąrašas
1. Užduoties tipo ir ID gavimas
2. Užduoties pradėjimas
3. Užduoties atlikimas

Visų užduočių sąrašas su pagrindine informacija (bet ne specifine) yra čia:

http://127.0.0.1:8000/api/challenge/

Vartotojui pasirinkus užduotį, turi būti sukuriamas objektas POST metodu į atitinkamos užduoties endpoint'ą:

Jei tipas yra "article":
http://127.0.0.1:8000/api/article_joined_challenge/

Turi būti siunčiami šie duomenys:

```json
{
        "main_joined_challenge": {
            "id": 2, 
            "uuid": "af7acf5c-24fd-404e-93be-97371faae793",
            "status": "completed",
            "user": 7,
            "challenge": 2
        },
    },```
