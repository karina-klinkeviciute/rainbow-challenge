from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=2000)
    country = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.name} - {self.country}"

