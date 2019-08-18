# Repository
- Clone repository `git clone https://github.com/vug/personalwebapp.git`

# Virtual environment

## Anaconda

- Create a new virtual `conda create --name personalwebapp python=3.5` (or whatever the latest version is, say 3.7)
- Activate environment. Windows: `activate personalwebapp`, OSX: `source activate personalwebapp`
- Deactive environment. Windows: `deactivate personalwebapp`, OSX: `source deactivate personalwebapp`

## Ubuntu

There is no Python 3.5 in `apt-get`. Download source code of release, for example [Python Release Python 3\.5\.2 \| Python\.org](https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz), from https://www.python.org/downloads/

First install the sqlite dependencies `sudo apt-get install libsqlite3-dev`

```
cd ~
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
tar -zvxf Python-3.5.2.tgz
mkdir python35
cd Python-3.5.2/
./configure --prefix=$HOME/python35 --enable-loadable-sqlite-extensions
make
make install
```
Now we have a working Python 3.5 executable at `~/python35/bin/python`. Use that to create a new virtual environment. `mkvirtualenv personalwebapp -p ~/python35/bin/python3`.

# Dependencies

## Production

- mikasa dependencies
  - On Windows install [Microsoft Visual C++ Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools) 
  - On Unix install `sudo apt-get install -y libffi-dev libssl-dev`
- `pip install -r requirements.txt`

## Development

### SQLite from command-line

Install [sqlite3](https://www.sqlite.org/cli.html) `sudo apt-get install sqlite3`
Connect to local sqlite database file `sqlite3 app.db`

Some commands

```
SELECT * from sqlite_master;
SELECT name FROM sqlite_master WHERE type='table';
SELECT * FROM user;
.exit
```

# Initialization

Create `secret_key` for Flask-Login security features, create SQLite database, create at least one user to be able to write blog posts.

```
python manage.py gen_secret
python manage.py create_db
python manage.py populate_db
python manage.py create_user --email johndoe@mail.com --password pass --fullname "John Doe" --timezone -5
```

# Unit Tests

At the project root directory, run `python -m unittest tests` or `python -m unittest --verbose tests`


# Run Application

- `python runserver.py`  runs in default port 8000
- `python runserver.py --port 8888`  to set the port number
- `gunicorn wsgi:app`  runs the app via gunicorn webserver
- `gunicorn -b :5000 wsgi:app`  set the port in gunicorn

# Supervisor

## Configuration

Supervisor configuration file `sudo vim /etc/supervisor/conf.d/personalwebapp.conf`

```
command = /home/ubuntu/.virtualenvs/personalwebapp/bin/gunicorn wsgi:app -w 3
directory = /home/ubuntu/personalwebapp
user = ubuntu
stdout_logfile = /home/ubuntu/personalwebapp/logs/gunicorn/gunicorn_stdout.log
stderr_logfile = /home/ubuntu/personalwebapp/logs/gunicorn/gunicorn_stderr.log
redirect_stderr = True
```

## Usage
Supervisor commands

```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start personalwebapp
sudo supervisorctl stop personalwebapp
sudo supervisorctl restart personalwebapp
```

# Misc

## SSH to EC2

create `~/.ssh/config` file on development machine to establish ssh connections easier.

```
Host mywebserver
    HostName IP_OF_EC2_INSTANCE
    User ubuntu # or ec2-user depending on the choice of AMI
    IdentityFile ~/.ssh/PRIVATE_KEY_FILE.pem
```
