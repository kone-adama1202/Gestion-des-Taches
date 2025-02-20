
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# 🔑 Connexion
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm


# taches/views.py
from django.shortcuts import render, get_object_or_404

from .forms import (
    InscriptionForm, ProjetForm, TacheForm, ProfilForm, CustomPasswordChangeForm
)
from .models import Tache, Projet

# 🔑 Inscription
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie.")
            return redirect('connexion')
        messages.error(request, "Corrigez les erreurs.")
    else:
        form = InscriptionForm()
    return render(request, 'taches/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accueil')  # Redirige vers la vue d'accueil
    else:
        form = AuthenticationForm()
    return render(request, 'taches/connexion.html', {'form': form})


# 🔑 Déconnexion
@login_required
def deconnexion(request):
    logout(request)
    messages.info(request, "🚪 Vous avez été déconnecté.")
    return redirect('connexion')

# 📝 Gestion du profil
@login_required
def modifier_profil(request):
    profil_form = ProfilForm(request.POST or None, request.FILES or None, instance=request.user)
    password_form = CustomPasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == 'POST':
        if 'modifier_infos' in request.POST and profil_form.is_valid():
            profil_form.save()
            messages.success(request, "✅ Profil mis à jour avec succès.")
            return redirect('profil')
        elif 'changer_mot_de_passe' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "🔒 Mot de passe mis à jour.")
            return redirect('profil')
        messages.error(request, "❌ Corrigez les erreurs.")

    return render(request, 'taches/modifier_profil.html', {
        'profil_form': profil_form,
        'password_form': password_form
    })

@login_required
def profil(request):
    return render(request, 'taches/profil.html', {'utilisateur': request.user})

# 📁 Gestion des projets
from django.shortcuts import render, redirect
from .forms import ProjetForm

def creer_projet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.createur = request.user  # Associe le projet à l'utilisateur connecté
            projet.save()
            return redirect('accueil')  # Redirige après création
    else:
        form = ProjetForm()

    return render(request, 'taches/creer_projet.html', {'form': form})



def modifier_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)

    if request.method == 'POST':
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            return redirect('detail_projet', projet_id=projet.id)
        else:
            print("Form errors:", form.errors)  # Affiche les erreurs dans la console
    else:
        form = ProjetForm(instance=projet)  # Important : passe l'instance ici

    return render(request, 'taches/modifier_projet.html', {'form': form, 'projet': projet})


@login_required
def supprimer_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    # 👉 Pas de restriction ici
    if request.method == 'POST':
        projet.delete()
        messages.success(request, "Projet supprimé avec succès.")
        return redirect('accueil')
    return render(request, 'taches/confirm_delete.html', {'projet': projet})


@login_required
def creer_projet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet.createur = request.user  # Assigner l'utilisateur connecté comme créateur du projet
            projet.save()
            messages.success(request, "✅ Projet créé avec succès.")
            return redirect('detail_projet', projet_id=projet.id)  # Rediriger vers le détail du projet
        else:
            messages.error(request, "❌ Corrigez les erreurs dans le formulaire.")
    else:
        form = ProjetForm()

    return render(request, 'taches/creer_projet.html', {'form': form})
@login_required
def detail_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    taches = projet.taches.all()
    return render(request, 'taches/detail_projet.html', {'projet': projet, 'taches': taches})



# 📝 Gestion des tâches dans un projet
@login_required
def creer_tache(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.projet = projet
            tache.save()
            messages.success(request, "✅ Tâche ajoutée.")
            return redirect('detail_projet', projet_id=projet.id)
        messages.error(request, "❌ Corrigez les erreurs.")
    else:
        form = TacheForm()
    return render(request, 'taches/creer_tache.html', {'form': form, 'projet': projet})

@login_required
def modifier_tache(request, tache_id):
    tache = get_object_or_404(Tache, id=tache_id)
    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Tâche modifiée.")
            return redirect('detail_projet', projet_id=tache.projet.id)
    else:
        form = TacheForm(instance=tache)
    return render(request, 'taches/modifier_tache.html', {'form': form, 'tache': tache})

@login_required
def supprimer_tache(request, tache_id):
    tache = get_object_or_404(Tache, id=tache_id)
    if request.method == 'POST':
        tache.delete()
        messages.success(request, "✅ Tâche supprimée.")
        return redirect('detail_projet', projet_id=tache.projet.id)
    return render(request, 'taches/supprimer_tache.html', {'tache': tache})


def accueil(request):
    projets = Projet.objects.filter(createur=request.user)
    return render(request, 'taches/accueil.html', {'projets': projets})


