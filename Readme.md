# TruckAPP
#### Um backend em python3 usando Swagger, Connexion, Flask, Peewee

### Instala virtual env no linux
sudo apt-get install python3.4-venv

### Clona projeto
git clone git@github.com:ajalbut/truckapp.git

### Inicializa venv no diretorio do projeto
cd truckapp
python3 -m venv venv
. venv/bin/activate

### Instala dependências
pip install Flask swagger_ui_bundle connexion peewee geopy

### Cria tabelas
python3 create_tables.py

### Roda servidor
python3 server.py

### Roda testes unitários
python3 tests.py

### Acessa serviços via api swagger
http://0.0.0.0:5000/api/ui
