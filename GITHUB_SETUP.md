# Instructions pour publier sur GitHub

## 1. Créer un nouveau dépôt sur GitHub

1. Allez sur https://github.com/new
2. Nommez votre dépôt (ex: `rag-pdf`)
3. Choisissez **Public** ou **Private**
4. **NE PAS** initialiser avec README, .gitignore ou licence (déjà présents)
5. Cliquez sur **Create repository**

## 2. Connecter le dépôt local à GitHub

```bash
# Remplacez VOTRE_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/VOTRE_USERNAME/rag-pdf.git

# Ou avec SSH (si configuré) :
# git remote add origin git@github.com:VOTRE_USERNAME/rag-pdf.git
```

## 3. Vérifier la configuration

```bash
git remote -v
```

## 4. Pousser le code

```bash
# Renommer la branche principale si nécessaire
git branch -M main

# Pousser le code
git push -u origin main
```

## 5. Vérifier sur GitHub

Allez sur https://github.com/VOTRE_USERNAME/rag-pdf pour voir votre code !

## ⚠️ Important

- Le fichier `.env` est **automatiquement ignoré** (ne sera pas commité)
- Ne partagez **JAMAIS** vos clés API publiquement
- Vérifiez que `.env` n'apparaît pas dans les fichiers commités

## Vérification

```bash
# Vérifier que .env n'est pas tracké
git ls-files | grep .env
# Ne doit rien retourner (ou seulement .env.example)
```

