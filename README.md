# Traffic-Access-Dashboard

*A simple dashboard created with Python 3.9.4 and Flask 2.0*

visualize the trends of the most used applications in some important cities of Venezuela as a network administrator in a telecommunications company (the measurements stored and displayed in this app are not real).

![alt text](https://raw.githubusercontent.com/metalpoch/Traffic-Access-Dashboard/main/Screenshot_2021-06-11%20TrafficAccess.png)

## Installation

##### Clone this repository [GitHub](https://github.com/metalpoch/Traffic-Access-Dashboard#) and create a virtual environment
```bash
git clone https://github.com/metalpoch/Traffic-Access-Dashboard.git
cd Traffic-Access-Dashboard/
python -m venv venv
source venv/bin/activate
```

##### Use [pip](https://pip.pypa.io/en/stable/) to install the modules in the file requirements.txt 
```bash
pip install -r requirements.txt
```

## Use
##### Using flask run
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

##### Using app.run()
```bash
python run.py
```

## Licence
[MIT](https://choosealicense.com/licenses/mit/)
