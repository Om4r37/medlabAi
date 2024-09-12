git clone https://github.com/Om4r37/medlabAi.git
cd medlabAi/app/
mkdir models
wget https://github.com/Om4r37/medlabAi/releases/download/v0.9/data.zip
unzip data.zip
rm -f data.zip
cd ..
pip install -r requirements.txt
wget https://github.com/Om4r37/medlabAi/releases/download/v0.9/users.sql
cd medlabAi/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py