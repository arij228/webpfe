# [Black Dashboard Flask](https://demos.creative-tim.com/black-dashboard/examples/dashboard.html) [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&logo=twitter)](https://twitter.com/intent/tweet?text=Black%20Dashboard%20by%20Creative%20Tim&url=https%3A%2F%2Fdemos.creative-tim.com%2Fblack-dashboard%2Fexamples%2Fdashboard.html&via=CreativeTim)


 ![version](https://img.shields.io/badge/version-1.0.1-blue.svg)  ![license](https://img.shields.io/badge/license-MIT-blue.svg) [![GitHub issues open](https://img.shields.io/github/issues/creativetimofficial/black-dashboard/issues.svg?maxAge=2592000)](https://github.com/creativetimofficial/black-dashboard/issues/issues?q=is%3Aopen+is%3Aissue) [![GitHub issues closed](https://img.shields.io/github/issues-closed-raw/creativetimofficial/black-dashboard/issues.svg?maxAge=2592000)](https://github.com/creativetimofficial/black-dashboard/issues/issues?q=is%3Aissue+is%3Aclosed) [![Join the chat at https://gitter.im/NIT-dgp/General](https://badges.gitter.im/NIT-dgp/General.svg)](https://gitter.im/creative-tim-general/Lobby) [![Chat](https://img.shields.io/badge/chat-on%20discord-7289da.svg)](https://discord.gg/E4aHAQy)


![Product Gif](https://s3.amazonaws.com/creativetim_bucket/github/gif/black-dashboard.gif)

Black Dashboard Flask est une application web intégrant le design Bootstrap 4 "Black Dashboard" avec un backend Flask. Cette application combine la beauté du design avec la puissance de Python Flask pour la gestion des utilisateurs et l'authentification sécurisée.

Le système inclut :
- Authentification utilisateur avec email et mot de passe
- Vérification par code OTP (One-Time Password)
- Interface administrateur élégante
- Base de données SQL Server via pyODBC
- Pages Dashboard et Profil utilisateur

Black Dashboard est conçu avec des couleurs agréables à l'œil, des cartes spacieuses, une belle typographie et des graphiques attrayants. Il est léger, facile à utiliser et très puissant.

Le dashboard est disponible en deux versions: Mode Sombre et Mode Clair.

Remerciements spéciaux à :
- [Robert McIntosh](https://github.com/mouse0270/bootstrap-notify) pour le système de notification.
- [Chartist](https://gionkunz.github.io/chartist-js/) pour les magnifiques graphiques.

## Table des matières

* [Démo](#demo)
* [Démarrage rapide](#démarrage-rapide)
* [Installation](#installation)
* [Fonctionnalités](#fonctionnalités)
* [Structure des fichiers](#structure-des-fichiers)
* [Support navigateur](#support-navigateur)
* [Ressources](#ressources)
* [Signaler un problème](#signaler-un-problème)
* [Support technique ou questions](#support-technique-ou-questions)
* [Licence](#licence)
* [Liens utiles](#liens-utiles)


## Démo

- [Page d'accueil](https://demos.creative-tim.com/black-dashboard/examples/dashboard.html)
- [Page profil utilisateur](https://demos.creative-tim.com/black-dashboard/examples/user.html)
- [Page tableaux](https://demos.creative-tim.com/black-dashboard/examples/tables.html)

[Voir plus](https://demos.creative-tim.com/black-dashboard/examples/dashboard.html).


## Démarrage rapide

- Cloner le repo: `git clone https://github.com/votreusername/black-dashboard-flask.git`.
- Installer les dépendances: `pip install -r requirements.txt`
- Configurer la connexion SQL Server dans `app.py`
- Lancer l'application: `python app.py`

## Installation

1. Assurez-vous que Python 3.6+ est installé
2. Installez les dépendances:
```
pip install flask pyodbc werkzeug
```
3. Configurez votre connexion SQL Server dans le fichier app.py:
```python
server = 'votre_serveur'  # Remplacez par votre serveur SQL
database = 'users'       # Nom de la base de données
```
4. Lancez l'application:
```
python app.py
```
5. Accédez à l'application à l'adresse http://127.0.0.1:5000

## Fonctionnalités

1. **Authentification utilisateur**:
   - Inscription avec email et mot de passe
   - Vérification par code OTP
   - Connexion sécurisée

2. **Interface dashboard**:
   - Vue d'ensemble des données
   - Profil utilisateur
   - Navigation intuitive

3. **Sécurité**:
   - Mots de passe hashés
   - Protection contre les attaques courantes
   - Gestion des sessions Flask

## Structure des fichiers
```
black-dashboard-flask/
├── CHANGELOG.md
├── README.md
├── static/
│   ├── css/
│   ├── demo/
│   ├── fonts/
│   ├── img/
│   ├── js/
│   └── scss/
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   └── user.html
├── app.py                # Application Flask principale
├── gulpfile.js
├── genezio.yaml
├── package.json
└── LICENSE.md
```

## Support navigateur

Nous visons officiellement à prendre en charge les deux dernières versions des navigateurs suivants:

<img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/chrome.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/firefox.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/edge.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/safari.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/opera.png" width="64" height="64">

## Signaler un problème

Nous utilisons GitHub Issues comme outil officiel de suivi des bugs. Voici quelques conseils:

1. Assurez-vous d'utiliser la dernière version de l'application.
2. Fournissez des étapes reproductibles pour réduire le temps de résolution.
3. Certains problèmes peuvent être spécifiques au navigateur, alors précisez dans quel navigateur vous avez rencontré le problème.

## Support technique ou questions

Si vous avez des questions ou besoin d'aide pour intégrer le produit, veuillez [nous contacter](mailto:votre-email@exemple.com) au lieu d'ouvrir un ticket.

## Licence

- Copyright 2019 Creative Tim (https://www.creative-tim.com/)
- Licence MIT (https://github.com/creativetimofficial/black-dashboard/issues/blob/master/LICENSE.md)

## Liens utiles

- [Plus de produits](https://www.creative-tim.com/bootstrap-themes) de Creative Tim
- [Tutoriels](https://www.youtube.com/channel/UCVyTG4sCw-rOvB9oHkzZD1w)
- [Freebies](https://www.creative-tim.com/bootstrap-themes/free) de Creative Tim
- [Programme d'affiliation](https://www.creative-tim.com/affiliates/new) (gagnez de l'argent)

##### Réseaux sociaux

Twitter: <https://twitter.com/CreativeTim>

Facebook: <https://www.facebook.com/CreativeTim>

Dribbble: <https://dribbble.com/creativetim>

Instagram: <https://instagram.com/creativetimofficial>