git clone https://github.com/Om4r37/medlabAi.git
cd medlabAi\app\
mkdir models
curl https://github.com/Om4r37/medlabAi/releases/download/v0.9/data.zip -UseBasicParsing -OutFile data.zip
tar -xf data.zip
del data.zip
cd ..
curl https://github.com/Om4r37/medlabAi/releases/download/v0.9/users.sql -UseBasicParsing -OutFile users.sql
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
start http://localhost:1337/
python run.py