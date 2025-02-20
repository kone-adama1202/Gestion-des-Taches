from django.contrib import admin

from taches.models import Tache, Projet


admin.site.register(Projet)
admin.site.register(Tache)
