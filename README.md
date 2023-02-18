# YOK Core app micro service
<hr />

Cette application est un microservice en charge de la gestion des portefeuilles d'un utilisateur.


### Technologies utilisées
>- Python 3.8+
>- Django rest framework


### Procédure d'Installation 
1. Clonage du projet en local
>`git clone git@gitlab.com:cryptoechangeur/microservices/core.git`.

2. Installation des dépendances
> `cd user_account` <br/>
> `pip install -r requirements.txt` <br/>

3. Configuration des variables d\'environement<br/>
Créer un fichier `.env` à la racine du projet et ajouter : __SECRET_KEY__, __WALLET_CREDIT_1__, __WALLET_CREDIT_1_USER__, __WALLET_CREDIT_2__, __WALLET_CREDIT_2_USER__, __WALLET_CLIENT_CREDIT_CODE__, __WALLET_DEBIT_1__, __WALLET_DEBIT_1_USER__, __WALLET_DEBIT_2__, __WALLET_DEBIT_2_USER__, __WALLET_CLIENT_DEBIT_CODE__. 
- Le __SECRET_KEY__ correspond à la clé secrete de l'application django. généré par la commande:<br/>
`python -c "import secrets; print(secrets.token_urlsafe())"`.
- Le __WALLET_CREDIT_1__ La référence du wallet de crédit de monnaie réelle
- Le __WALLET_CREDIT_1_USER__ La référence de l'utilisateur qui possède le wallet de crédit de monnaie réelle
- Le __WALLET_CREDIT_2__ La référence du wallet de crédit de crypto monnaie
- Le __WALLET_CREDIT_2_USER__ La référence de l'utilisateur qui possède le wallet de crédit de crypto monnaie
- Le __WALLET_CLIENT_CREDIT_CODE__ Le code Client de wallet de credit
- Le __WALLET_DEBIT_1__ La référence du wallet de débit de monnaie réelle
- Le __WALLET_DEBIT_1_USER__ La référence de l'utilisateur qui possède le wallet de débit de monnaie réelle
- Le __WALLET_DEBIT_2__ La référence du wallet de débit de crypto monnaie
- Le __WALLET_DEBIT_2_USER__ La référence de l'utilisateur qui possède le wallet de débit de crypto monnaie
- Le __WALLET_CLIENT_DEBIT_CODE__ Le code Client de wallet de débit

> *<u>Exemple de fichier __.env__</u> :* <br/>
> DEBUG=True <br/>
> SECRET_KEY = 'bfQspVSh90eG3yrQo8lBZjKLfkDCsjwXvA9Gmc12cUo' <br/>
> WALLET_CREDIT_1 = 'xxxxxxxxxxxxx' <br/>
> WALLET_CREDIT_1_USER = 'xxxxxxxxxxxxx' <br/>
> WALLET_CREDIT_2 = 'xxxxxxxxxxxxx' <br/>
> WALLET_CREDIT_2_USER = 'xxxxxxxxxxxxx' <br/>
> WALLET_CLIENT_CREDIT_CODE = 0000 <br/>
> WALLET_DEBIT_1 = 'xxxxxxxxxxxxx' <br/>
> WALLET_DEBIT_1_USER = 'xxxxxxxxxxxxx' <br/>
> WALLET_DEBIT_2 = 'xxxxxxxxxxxxx' <br/>
> WALLET_DEBIT_2_USER = 'xxxxxxxxxxxxx' <br/>
> WALLET_CLIENT_DEBIT_CODE = 0000 <br/>



### Migration des tables
> `python manage.py makemigrations`<br/>
> `python manage.py migrate`<br/>
> 
### Exécuter les tests <em>(10 tests)</em>
> `python manage.py test`<br/>


### Création des modèles de base 
> `python manage.py factory -d 'wallet'`<br/>


### Démarrage du service 
> `python manage.py runserver`<br/>


### Routes URL
> *http://localhost:8000/apis/v1/wallet/create/ <br/>
> *http://localhost:8000/apis/v1/wallet/detail/<user_id> <br/>
> *http://localhost:8000/apis/v1/wallet/activate/ <br/>
> *http://localhost:8000/apis/v1/wallet/activate/ <br/>
> *http://localhost:8000/apis/v1/wallet/token/activate/ <br/>
> *http://localhost:8000/apis/v1/operations/fiat/topup/" <br/>
> *http://localhost:8000/apis/v1/operations/fiat/wire-transfer/" <br/>
> *http://localhost:8000/apis/v1/operations/fiat/withdraw/" <br/>
> *http://localhost:8000/apis/v1/operations/token/topup/" <br/>
> *http://localhost:8000/apis/v1/operations/token/wire-transfer/" <br/>
> *http://localhost:8000/apis/v1/operations/token/withdraw/" <br/>

Tous est ready !
