# instala virtual env no linux
sudo apt-get install python3.4-venv

# clona projeto

# inicializa venv no diretorio do projeto
mkdir truckapp

# inicializa venv no diretorio do projeto
cd truckapp
python3 -m venv venv
. venv/bin/activate

# instala dependências
pip install Flask
pip install swagger_ui_bundle
pip install connexion
pip install peewee
pip install geopy

# cria tabelas
python3 create_tables.py

# roda servidor
python3 server.py

# roda testes unitários

# acessa serviços via api swagger
http://localhost:5000/api/ui
