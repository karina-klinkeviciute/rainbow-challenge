import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models.base import BaseChallenge


class EventParticipantChallenge(BaseChallenge):
    """Event participant challenge is when you
    participate in some event organized by others"""
    event_name = models.CharField(
        max_length=1000,
        verbose_name=_("event name")
    )
    date = models.DateField(
        verbose_name=_("date"),
        null=True,
        blank=True
    )
    url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("link to the event"))
    qr_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("QR code")
    )
    # todo padaryti protected
    qr_code_file = models.ImageField(
        verbose_name=_("QR code file"),
        upload_to="qrcodesimages",
        blank=True,
        null=True
    )



# django admin command - generuoti QR kodą

# Tada prie challenge atsiranda QR kodas kaip failas

#   todo   padarom ir kur nors qr code generavimą, iš kur renginio organizatoriai galėtų jį parsisiųsti/atsispausdinti
# Kai vartotojas nuskenuoja QR kodą, jis siunčiamas į joined challenge.
# Ten gal saugomas, o gal tik patikrinamas (sutikrinamas su kodu, esančiu ant challenge) ir tada pažymima varnelė, kad atlikta.
# Dėl visa ko, galima būtų padaryti, kad kodą galima būtų suvesti ir ranka - nežinau ar tada nebūtų taip, kad juo būtų dalijamasi

# Jei QR kodas kažkodėl nenusiskenuoja, tada reikėtų daryti atvirkščiai - kad renginio organizatoriai gautų kodą iš vartotojo ir pasižymėtų jį?

# Gal foto tiktų kaip įrodymas, kad tikrai dalyvavo, jei nėra galimtybės qr kodo skenuoti?
