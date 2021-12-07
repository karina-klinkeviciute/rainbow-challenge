
## Užduočių informacija

Visų užduočių sąrašas su pagrindine informacija (bet ne specifine) yra čia:

http://rainbowchallenge.lt/api/challenge/

Užduotis identifikuojama pagal lauką `uuid`

## Užduoties pradėjimas

### Užduočių pradėjimo eiga pagal skirtingus kriterijus

Kai kurios užduotys gali būti atliekamos tik vieną kartą, kitos - kelis kartus. 

Užduočių sąraše yra šie indikatoriai

* `multiple` - ar užduotis gali būti atliekama daugiau nei vieną kartą. `true` - gali, `false` - negali.
* `can_be_joined` - ar prisijungęs naudotojo gali pradėti naują šią užduotį
* `is_joined` - ar prisijungusi naudotoja yra pradėjusi naują užduotį. Atliktos užduotys čia yra `false`, tik pradėtos bet dar neatliktos yra `true`
* `joined_concrete_challenges` - prisijungusio naudotojo visos pradėtos užduotys, pagal tipą. t.y., čia grąžinami uuid konkrečios užduoties, pavyzdžiui jei tipas yra `event`, čia grąžinamas `event_joined_challenge` objekto uuid.

Pagal šiuos kriterijus, galimi keli scenarijai:
1. Užduotis nėra ir nebuvo pradėta 

    Šiuo atveju pradedama nauja užduotis. (siunčiama POST užklausa į konkretaus tipo endpontą, pvz `event_participant_joined_challenge`)
    Indikatorius `can_be_joined` šiuo atveju bus `true` o `is_joined` - `false`
2. Užduotis pradėta bent vieną kartą
   1. užduotį galima atlikti tik vieną kartą (indikatorius `'multiple` yra `false`). Šiuo atveju `can_be_joined` bus `false`, `is_joined` bus `true`. Taip pat bus sąrašas `concrete_joined_challenges` tik su vienos užduoties uuid. Pagal šį uuid ir challenge tipą reikia susirasti pradėtą užduotį (joined challenge) ir jį rodyti. Pavyzdžiui, tai gali būti `event_participant_joined_challenge` su šiuo uuid.
   2. užduotį galima atlikti daugiau nei vieną kartą (indikatorius `multiple` yra `true`, `can_be_joined` - `true`, `is_joined` - `true`). Tokiu atveju `concrete_joined_challenges` bus sąrašas su viena ar daugiau pradėtų užduočių (jų uuid). Šiuo atveju reikia paklausti vartotojo, ar jis nori pradėti naują užduotį, ar tęsti esamą. 
      1. Jei pasirenka "pradėti naują" - viskas atliekama kaip pirmam žingsnyje
      2. Jei pasirenkama "tęsti pradėtą" - vartotojas nukeliamas į puslapį Pradėtos užduotys. Čia galės pasirinkti, kurią pradėtą užduotį tęsti.
      

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
http://127.0.0.1:8000/api/event_participant_joined_challenge/

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

