
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.conf import settings
from datetime import date
from django.db import models

class Projet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_debut = models.DateField(default=date(2025, 1, 1))  # Utilise un objet date pour la valeur par défaut
    date_fin = models.DateField(default=date(2025, 12, 31))  # Utilise un objet date pour la valeur par défaut
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projets_crees')

    def __str__(self):
        return self.nom


# taches/models.py
class Tache(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    assigne_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='taches', null=True, blank=True)

    date_echeance = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nom


    from django.contrib.auth.models import User

    class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        role = models.CharField(max_length=10, choices=[('professeur', 'Professeur'), ('etudiant', 'Étudiant')])
        avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

        def __str__(self):
            return self.user.username

    class ProjetForm(forms.ModelForm):
        class Meta:
            model = Projet
            fields = ['nom', 'description', 'date_debut',
                      'date_fin']  # Assure-toi d'inclure tous les champs nécessaires







