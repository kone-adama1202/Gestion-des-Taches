from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

urlpatterns = [
    # 🔑 Authentification
    path('', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('logout/', LogoutView.as_view(next_page='connexion'), name='logout'),

    # 🏠 Accueil
    path('accueil/', views.accueil, name='accueil'),

    # 📁 Gestion des projets
    path('creer_projet/', views.creer_projet, name='creer_projet'),
    path('projet/<int:projet_id>/', views.detail_projet, name='detail_projet'),
    path('projet/<int:projet_id>/creer_tache/', views.creer_tache, name='creer_tache'),

path('projet/modifier/<int:projet_id>/', views.modifier_projet, name='modifier_projet'),
    path('projet/supprimer/<int:projet_id>/', views.supprimer_projet, name='supprimer_projet'),




    # 👤 Gestion du profil
    path('profil/', views.profil, name='profil'),
    path('modifier_profil/', views.modifier_profil, name='modifier_profil'),  # Ajout de cette ligne
]
