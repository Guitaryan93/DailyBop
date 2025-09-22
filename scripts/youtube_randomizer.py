# YouTube Music Randomizer. Get new artists you never heard of! Like shopping
# in HMV or on iTunes back in the olden' times...

from ytmusicapi import YTMusic
from random import randint
import json
from pathlib import Path
import sqlite3
import requests


class RandomGenerator():
    def __init__(self):
        self.ytmusic = YTMusic()
        self.BASE_DIR = Path(__file__).resolve().parent
        self.DB_PATH = self.BASE_DIR/".."/"database"/"database.db"
        eng_dict = self.load_english_dictionary()
        self.search_string = self.generate_search_string(eng_dict)
        self.random_result = self.call_YT_API()
        self.get_streaming_services_urls()

        #for k, v in self.random_result.items():
        #    print(k, v)

        #print("\n\n==========================================================================\n\n")

        #print(json.dumps(self.random_result, indent=4))

        self.write_to_db()

    def load_english_dictionary(self):
        ''' load large file of all english words and then pare it down to
            just the words without the other json/dictionary data '''
        with open(f"{self.BASE_DIR}/words_dictionary.json", "r") as file:
            eng_dictionary = json.load(file)
        return list(eng_dictionary.keys())

    def generate_search_string(self, wordlist):
        ''' generate a 5 character string to use as a search term with
            YouTube Music API '''
        search_string = wordlist[randint(0, len(wordlist) - 1)]
        return search_string[0:5]

    def call_YT_API(self):
        ''' call the YouTube Music API, pull a random artist, update the data with
            the YouTube Music Video URL (used to call songlink API next) '''
        YTMusicAPIdata = self.ytmusic.search(self.search_string, "songs", limit=200)
        random_artist = YTMusicAPIdata[randint(0,len(YTMusicAPIdata) - 1)]
        random_artist.update({"YT_url": f"https://music.youtube.com/watch?v={random_artist.get('videoId')}",
                              "YT_embed": f"https://www.youtube.com/embed/{random_artist.get('videoId')}"})

        #for k, v in random_artist.items():
        #    print(k, v)

        return random_artist

    def get_streaming_services_urls(self):
        ''' call song.link API to get all other major streaming services URLs
            AND a better thumbnail image than the YTMusic one...
            1. Spotify = BEST
            2. Amazon Music
            3. YTMusic = WORST (default if no other results are available) '''
        url = "https://api.song.link/v1-alpha.1/links"
        params = {
            "url": self.random_result.get("YT_url"),
            "userCountry": "CA",
            "songIfSingle": "true"
        }
        res = requests.get(url, params=params)
        data = res.json() 

        services = [
            {"key": "youtube", "label": "YouTube", "icon": "youtube.svg"},
            {"key": "youtubeMusic", "label": "YouTube Music", "icon": "ytmusic.svg"},
            {"key": "appleMusic", "label": "Apple Music", "icon": "applemusic.svg"},
            {"key": "spotify", "label": "Spotify", "icon": "spotify.svg"},
            {"key": "pandora", "label": "Pandora", "icon": "pandora.svg"},
            {"key": "deezer", "label": "Deezer", "icon": "deezer.svg"},
            {"key": "soundcloud", "label": "SoundCloud", "icon": "soundcloud.svg"},
            {"key": "amazonMusic", "label": "Amazon Music", "icon": "amazonmusic.svg"},
            {"key": "tidal", "label": "TIDAL", "icon": "tidal.svg"},
            {"key": "audiomack", "label": "Audiomack", "icon": "audiomack.svg"},
        ]
    
        # Filter only services that exist in the API response
        links = []
        for s in services:
            link = data["linksByPlatform"].get(s["key"], {}).get("url")
            if link:
                links.append({**s, "url": link})
    
        # Thumbnail fallback (Spotify → Amazon → YouTube Music)
        entities = data["entitiesByUniqueId"]
        thumbnail = None
        if "spotify" in data["linksByPlatform"]:
            uid = data["linksByPlatform"]["spotify"]["entityUniqueId"]
            thumbnail = entities.get(uid, {}).get("thumbnailUrl")
        if not thumbnail and "amazonMusic" in data["linksByPlatform"]:
            uid = data["linksByPlatform"]["amazonMusic"]["entityUniqueId"]
            thumbnail = entities.get(uid, {}).get("thumbnailUrl")
        if not thumbnail:
            thumbnail = self.random_result["thumbnails"][-1]["url"]

        self.random_result.update({"links": links, "thumbnail": thumbnail})

    def write_to_db(self):
        ''' pull out the data we need for our DB record and write it to the DB '''
        artist_name = self.random_result["artists"][0]["name"]
        song_title = self.random_result.get("title")
        thumbnail = self.random_result.get("thumbnail")
        YT_embed = self.random_result.get("YT_embed")

        # Turn links list into a dict of {key: url}
        links_dict = {link["key"]: link["url"] for link in self.random_result.get("links", [])}
        
        # Extract each service (return None if missing)
        youtube  = links_dict.get("youtube")
        youtubeMusic = links_dict.get("youtubeMusic")
        appleMusic = links_dict.get("appleMusic")
        spotify  = links_dict.get("spotify")
        pandora = links_dict.get("pandora")
        deezer   = links_dict.get("deezer")
        soundcloud = links_dict.get("soundcloud")
        amazonMusic = links_dict.get("amazonMusic")
        tidal = links_dict.get("tidal")
        audiomack = links_dict.get("audiomack")

        # write the new artist data to the database for the website to use
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()

        # Setup the DB table if it doesn't already exist
        cur.execute("""
        CREATE TABLE IF NOT EXISTS random_artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            song_title TEXT,
            thumbnail TEXT,
            YT_embed TEXT,
            youtube TEXT,
            youtubeMusic TEXT,
            appleMusic TEXT,
            spotify TEXT,
            pandora TEXT,
            deezer TEXT,
            soundcloud TEXT,
            amazonMusic TEXT,
            tidal TEXT,
            audiomack TEXT,
            date_added DATE DEFAULT (DATE('now'))
        )
        """)

        cur.execute("""
        INSERT INTO random_artists
        (name, song_title, thumbnail, YT_embed, youtube, youtubeMusic, appleMusic, spotify, pandora, deezer, soundcloud, amazonMusic, tidal, audiomack)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            artist_name,
            song_title,
            thumbnail,
            YT_embed,
            youtube,
            youtubeMusic,
            appleMusic,
            spotify,
            pandora,
            deezer,
            soundcloud,
            amazonMusic,
            tidal,
            audiomack
        ))

        conn.commit()
        conn.close()


if __name__ == "__main__":
    app = RandomGenerator()

