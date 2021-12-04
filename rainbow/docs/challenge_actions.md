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
        "challenge": null
    },
    "article_name": "",
    "article_url": ""
}
```

Būtini duomenys: 
challenge - užduoties `uuid`

### Dalyvavimas renginyje

Jei tipas yra "event":
http://127.0.0.1:8000/api/article_joined_challenge/

Turi būti siunčiami šie duomenys:

```json
{
        "main_joined_challenge": {
            "status": "joined",
            "challenge": "cbed2257-98f4-4be3-a894-66f05600db25"
        }
    }
```

Būtini duomenys: 
challenge - užduoties `uuid`

## Užduoties atlikimas

užduotis atliekama pakeičiant jos būseną iš `joined` į `completed` per šį endpoint su `PATCH` metodu:

http://127.0.0.1:8000/api/article_joined_challenge/<uuid>/

Jei norim pažymėti užduoti, kurios konkrečios užduoties ID yra 33286b1c-c5c6-4e50-a1ab-73259309a38a tai reikia į šį endpoint:

http://127.0.0.1:8000/api/article_joined_challenge/33286b1c-c5c6-4e50-a1ab-73259309a38a/

paduoti šiuos duomenis per `PATCH` metodą:

```json
  {
    "main_joined_challenge": {
      "status": "completed"
    }

  }
```

## Informacijos apie užduotį gavimas

Jei norim gauti informaciją apie vieną konkrečią užduotį, pavyzdžiui vieną straipsnio rašymo užduotį, reikia kreiptis su `GET` metodu į jos endpoint:

http://127.0.0.1:8000/api/article_challenge/<uuid>/

Pavyzdžiui: 

http://rainbowchallenge.lt/api/article_challenge/8beb0f51-2438-413a-9f36-9e2813a919e8/


## Informacijos apie pradėtą/atliktą užduotį gavimas

kreipiamasi `GET` metodu į šį endpoint

http://127.0.0.1:8000/api/article_joined_challenge/<uuid>/

pavyzdžiui: http://127.0.0.1:8000/api/article_joined_challenge/33286b1c-c5c6-4e50-a1ab-73259309a38a/

