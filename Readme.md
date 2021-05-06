# Ponzi

After cloning , intialize new virtual env.

```sh
$ cd ponzi_folder
$ python3 -m venv venv_ponzi
```
Now the virtual env is all set. All you have to do is activate it.
Windows activation:
```
$ cd venv/Scripts/Activate
```
Linux:
```
$  source venv/bin/activate
```
Once activated navigate back to root directory and install all dependencies.
```
(venv) $ pip install -r requirements.txt
```

Create .evn file , check the .env.example and configure the env variables in brand new .env file in root directory.


----
Firebase , you will need to leave firebase configuration object in following folders you will find variable 
firebase_config.

```
app/firebase_utils/db.py the firebase_config variable as at top of the script.
app/templates/join.html the firebase_config var is at very begging of JS inside HTML.
app/templates/ranking.html same as the join.html
```

Once you did that go to firebase console on the web page , find database and there is tab "RULES". Click on it and copy the following json object inside it in order to make app queries work.

```
{
  "rules": {
    "game": {
      "$uid":{
    "players": {
      ".indexOn": ["payment", "end_time", "position"],
    },
    },
    },
    ".read": true,
    ".write": true,
  }
}
```

That should be enough for app to start and now there is only one thing left. The /admin view is not on the  index page you have to go to it manually so in order to create a new game room please go for localhost:5000/admin. There will be form presisted and once submited it will create a new lobby wich will be shown once you refresh to index page ( localhost:5000/ ).


---

In order to run the application activate the virtual env and type following commands in terminal.

```
export FLASK_APP=run.py
flask run
```
If you are using windows just use set instead of export.














