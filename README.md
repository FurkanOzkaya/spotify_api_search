# Spotify API Search

Trying Spotify search API and returning 10 random music with specific genre with specific artists.

You can display genres and artists in core.constants.py.



# Deploy

## Manual Deploy
Export or assign below variable in spotify_api.settings.py

```
SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET
SPOTIFY_TRACK_LIMIT (default 50)
```

```
python manage.py runserver (or vscode run section can be used.)
```

---
## Docker

generate your own .env file from .env.example file. (copy and change the naming)

```
docker build -t spotify_api .
docker run -p 8000:8000 --env-file=.env spotify_api
```


---
# TEST

```
http://127.0.0.1:8000/api/tracks/rock
```