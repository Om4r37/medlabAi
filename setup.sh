git clone https://github.com/Om4r37/medlabAi.git
cd medlabAi/app/
mkdir models
wget https://github.com/Om4r37/medlabAi/releases/download/v0.9/data.zip
unzip data.zip
rm -f data.zip
cd ..
wget https://github.com/Om4r37/medlabAi/releases/download/v0.9/users.sql
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
xdg-open http://localhost:1337/
python3.10 run.py