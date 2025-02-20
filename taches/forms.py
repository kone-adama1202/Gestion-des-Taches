# taches/forms.py
from cProfile import Profile

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Projet, Tache
from django.shortcuts import render, redirect
from django.contrib.auth import login
# 🔑 Formulaire d’inscription
# forms.py


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)  # Inclure request.FILES pour les fichiers
        if form.is_valid():
            user = form.save()  # Enregistrer l'utilisateur
            # Créer le profil associé
            Profile.objects.create(user=user, role=form.cleaned_data['role'], avatar=form.cleaned_data.get('avatar'))
            login(request, user)  # Connecter l'utilisateur après l'inscription
            return redirect('dashboard')  # Rediriger vers le tableau de bord ou une autre page
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})

# 📝 Formulaire de projet
class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom du projet', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description du projet', 'class': 'form-control', 'rows': 4}),
        }

# 📝 Formulaire de tâche
class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = ['nom', 'description', 'assigne_a', 'date_echeance']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom de la tâche', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description de la tâche', 'class': 'form-control', 'rows': 4}),
            'assigne_a': forms.Select(attrs={'class': 'form-control'}),
            'date_echeance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

# 🧑‍💼 Formulaire de modification de profil
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class ProfilForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Ancien mot de passe")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Nouveau mot de passe")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmez le nouveau mot de passe")

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    ROLE_CHOICES = [('Etudiant', 'Étudiant'), ('Professeur', 'Professeur')]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'avatar')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.create(user=user, role=self.cleaned_data['role'])
            profile.avatar = self.cleaned_data.get('avatar')  # Enregistrez l'avatar
            profile.save()
        return user


