# Employee Punch Clock
A **very** simple employee punch clock software, consisting of a simple REST API. 

## Requirements
- Unix-like OS (FreeBSD/Linux/MacOS)
- [Python][get Python] >= 3.7
  - [Python requirements (`requirements.txt`)][requirements.txt]
- SQLite 3 (`sqlite-devel` / `libsqlite3-dev`)
- [Docker][get Docker] (optional)
  - [Docker compose][get Docker compose] (optional)

## How to install
### First steps
Using your favorite terminal emulator, run the following commands:
- Clone the project on designated directory:
```bash
git clone git@github.com:Zuquim/punch_clock.git
```
- Change directory to project root:
```bash
cd punch_clock
```
- Edit `config.py` replacing values according to your needs:
```bash
vim config.py
```

### Using ctrl script
Using your favorite terminal emulator, run the following command:
```bash
bash ctrl-punch-clock.bash
```
Options:
```
build       - Build Docker image
rebuild     - Re-Build Docker image (based on the one built with 'build')
run         - Run production Docker container
test        - Run py.test and remove container
update      - stop and remove running container -> 'rebuild' -> 'run'   
full-update - stop and remove running container ->  'build'  -> 'run'   
```

### Quick test run (development)
It will create the necessary local directories and Python venv, and run default 
Flask server on http://localhost:8000 (biding=`0.0.0.0:8000`).
You may edit [`run_development_mode.bash`][run_development_mode.bash] to fit 
your particular needs.

Using your favorite terminal emulator, run the following command:
```bash
bash run_develoment_mode.bash
```

### Running it (production)
#### [Docker compose][get Docker compose]:

Using your favorite terminal emulator, run the following command:
```bash
docker-compose up -d --build
```

#### [Docker][get Docker]:
- Build Docker image:
```bash
docker build --rm --pull --no-cache -t punch-clock:latest .
````
- Run Docker container (replace `<hostname>` with your local server hostname):
```bash
docker run -d -h <hostname> \
           --name punch-clock \
           -v /var/log:/var/log/api \
           -v /var/db:/var/db \
           -p 80:80 \
           punch-clock:latest
``` 

#### [Python venv][venv docs]:
Using your favorite terminal emulator, run the following commands:
- Create the necessary Python venv
```bash
python3 -m venv venv
```
- Activate virtual environment
```bash
source venv/bin/activate
```
- Update venv's pip and setuptools
```bash
pip3 install -U pip setuptools
```
- Install required packages in [`requirements.txt`][requirements.txt]
```bash
pip3 install -r requirements.txt
```
- Run tests
```bash
py.test
```
- Run [Gunicorn][gunicorn] server
```bash
gunicorn --threads=4 \
         --bind=0.0.0.0:80 \
         --access-logfile=/var/log/api/access.log \
         --error-logfile=/var/log/api/error.log \
         --log-level=info \
         punch_clock:app
```

## API Endpoints summary
- `/api/get/user/` => API path to get user data
- `/api/list/punches/user/` => API path to get all user's punches data
- `/api/list/users` => API path to get all users' data
- `/api/new/punch` => API path to create new punch
- `/api/new/user` => API path to create new user
- `/api/update/user` => API path to update user's attributes
---

## /api/get/user/`uid`
- HTTP Method: GET
- About: returns a JSON with user (`uid`) and some info

## /api/list/punches/user/`uid`
- HTTP Method: GET
- About: returns a JSON with a list of registered punches for user (`uid`)

## /api/list/users
- HTTP Method: GET
- About: returns a JSON with a list of registered users and their data

## /api/new/punch
- HTTP Method: POST
- About: create a new punch (in/out) for a user
- Required JSON content:
```json
{
  "user_id": 1,
  "punch_type": "in"
}
```

## /api/new/user
- HTTP Method: POST
- About: create a new user
- Required JSON content:
```json
{
  "full_name": "Full User Name",
  "cpf": "12345678900",
  "email": "user@domain.com"
}
```

## /api/update/user
- HTTP Method: POST
- About: updates user attributes based on JSON content
- Required JSON content:
```json
{
  "user_id": 1
}
```
- Optional content:
```json
{
  "full_name": "Full User Name",
  "cpf": "12345678900",
  "email": "user@domain.com"
}
```

---

[get Python]: https://www.python.org/downloads/
[get Docker]: https://docs.docker.com/get-docker/
[get Docker compose]: https://docs.docker.com/compose/install/
[venv docs]: https://docs.python.org/3/tutorial/venv.html
[gunicorn]: https://gunicorn.org/
[requirements.txt]: https://github.com/Zuquim/punch_clock/blob/master/requirements.txt
[run_development_mode.bash]: https://github.com/Zuquim/punch_clock/blob/master/run_development_mode.bash