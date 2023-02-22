# YOK Wallet Manager micro service
<hr />

Cette application est un microservice en charge de la gestion des portefeuilles d'un utilisateur.


### Technologies utilisées
>- Python 3.8+
>- Django rest framework


### Procédure d'Installation 
1. Clonage du projet en local
>`git clone git@gitlab.com:cryptoechangeur/microservices/wallet_manager.git`.

2. Installation des dépendances
> `cd wallet_manager` <br/>
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
```python
DEBUG=True 
SECRET_KEY = 'bfQspVSh90eG3yrQo8lBZjKLfkDCsjwXvA9Gmc12cUo' 
WALLET_CREDIT_1 = 'xxxxxxxxxxxxx' 
WALLET_CREDIT_1_USER = 'xxxxxxxxxxxxx' 
WALLET_CREDIT_2 = 'xxxxxxxxxxxxx' 
WALLET_CREDIT_2_USER = 'xxxxxxxxxxxxx' 
WALLET_CLIENT_CREDIT_CODE = 0000 
WALLET_DEBIT_1 = 'xxxxxxxxxxxxx' 
WALLET_DEBIT_1_USER = 'xxxxxxxxxxxxx' 
WALLET_DEBIT_2 = 'xxxxxxxxxxxxx' 
WALLET_DEBIT_2_USER = 'xxxxxxxxxxxxx' 
WALLET_CLIENT_DEBIT_CODE = 0000 
```


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
#### > http://localhost:8000/apis/v1/wallet/create/ (POST)<br/>
<i>Payload:</i>
``` json
// Payload : 
{
    "owner_ref": "<OWNER_REF>"
}
```

<i>Response:</i>
``` json
// Response: 
{
    "owner_ref": "<OWNER_REF>", 
    "amount": "0.0"
}
```

<br />


#### > http://localhost:8000/apis/v1/wallet/detail/<user_id> (GET)<br/>
<i>Response:</i>
``` json 
// Response 
{
    "amount": "0.0", 
    "tokens": [
        {
            "token_symbol": "<TOKEN_SYMBOLE>", 
            "token_ref": "<TOKEN_REF>", 
            "amount": 0.0, 
            "fiat_value": 0.0, 
            "fiat_value_currency": 0.0, 
            "is_active": true, 
            "activated_date": "<ACTIVATE_DATE>"
        }
    ]
}   
```

<br />


#### > http://localhost:8000/apis/v1/wallet/activate/ (POST)<br/>
<i>Payload:</i>
``` json
// Payload
{
    "owner_ref": "<OWNER_REF>"
} 
```

<i>Response:</i> 
``` json
// Response: 
{
    "owner_ref": "<OWNER_REF>", 
    "amount": "0.0"
}  
```
<br />

#### > http://localhost:8000/apis/v1/wallet/token/activate/ (POST) <br/>
<i>Payload:</i>
``` json
// Payload
{
    "token_symbol": "<TOKEN_SYMBOLE>",
    "owner_ref": "<OWNER_REF>",
    "wallet_ref": "<WALLET_REF>",
    "token_ref": "<TOKEN_REF>"
} 
```

<i>Response:</i> 
``` json
// Response: 
{
    "token_symbol": "<TOKEN_SYMBOLE>",
    "token_ref": "<TOKEN_REF>",
    "wallet_ref": "<WALLET_REF>",
    "owner_ref": "<OWNER_REF>",
    "amount": 0.0,
    "fiat_value": 0.0,
    "is_active": true,
    "activated_date": "<ACTIVATED_DATE>"
}  
```
<br />

#### > http://localhost:8000/apis/v1/operations/fiat/topup/" (POST) <br/>
<i>Payload:</i>
``` json
// Payload
{
    "ops_type": "FIAT_TOP_UP",
    "from_wallet": "<FROM_WALLET>",
    "to_wallet": "<TO_WALLET>",
    "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
    "token_code": "FIAT",
    "amount": 1200.80,
    "payment": {
        "operator": "MOMO",
        "name": "OM",
        "phone_number": "0640509688",
    }
} 
```

<i>Response:</i> 
``` json
// Response: 
{
    "message": "Success",
    "operation": "FIAT_TOP_UP"
}  
```
<br />

#### > http://localhost:8000/apis/v1/operations/fiat/wire-transfer/" (POST) <br/>
<i>Payload:</i>
``` json
// Payload
{
    "ops_type": "FIAT_WIRE_TRANSFER",
    "from_wallet": "<FROM_WALLET>",
    "to_wallet": "<TO_WALLET>",
    "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
    "token_code": "FIAT",
    "amount": 2500.80,
    "payment": {
        "operator": "MOMO",
        "name": "OM",
        "phone_number": "0640509688",
    }
} 
```

<i>Response:</i> 
``` json
// Response: 
{
    "message": "Success",
    "operation": "FIAT_WIRE_TRANSFER"
}  
```
<br />

#### > http://localhost:8000/apis/v1/operations/fiat/withdraw/" (POST) <br/>
<i>Payload:</i>
``` json
// Payload
{
    "ops_type": "FIAT_WITHDRAW",
    "from_wallet": "<FROM_WALLET>",
    "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
    "token_code": "FIAT",
    "amount": 74500.80
} 
```

<i>Response:</i> 
``` json
// Response: 
{
    "message": "Success",
    "operation": "FIAT_WITHDRAW"
}  
```
<br />

#### > http://localhost:8000/apis/v1/operations/token/topup/" (POST)<br/>
<i>Payload:</i>
``` json
// Payload
{
    "ops_type": "TOP_UP",
    "to_wallet": "<TO_WALLET>",
    "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
    "token_code": "BTC",
    "amount": 1200.80,
    "payment": {
        "operator": "MOMO",
        "name": "OM",
        "phone_number": "0640509688",
    }
} 
```

<i>Response:</i> 
``` json
// Response: 
{
    "message": "Success",
    "operation": "TOP_UP"
}  
```
<br />

#### > http://localhost:8000/apis/v1/operations/token/wire-transfer/" (POST)<br/>
<i>Payload:</i>
``` json
// Payload
{
    "ops_type": "WIRE_TRANSFER",
    "from_wallet": "<FROM_WALLET>",
    "to_wallet": "<TO_WALLET>",
    "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
    "token_code": "FIAT",
    "amount": 2500.80,
    "payment": {
        "operator": "MOMO",
        "name": "OM",
        "phone_number": "0640509688",
    }
} 
```

<i>Response:</i> 
``` json
// Response: 
{
    "message": "Success",
    "operation": "WIRE_TRANSFER"
}  
```
<br />

#### > http://localhost:8000/apis/v1/operations/token/withdraw/" (POST)<br/>
<i>Payload:</i>
``` json
// Payload
{
    "ops_type": "WITHDRAW",
    "from_wallet": "<FROM_WALLET>",
    "to_external_wallet": "<EXTERNAL_WALLET>",
    "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
    "token_code": "FIAT",
    "amount": 74500.80
} 
```

<i>Response:</i> 
``` json
// Response: 
{
    "message": "Success",
    "operation": "WITHDRAW"
}  
```
<br />

Tous est ready !
