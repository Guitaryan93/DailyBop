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
        self.random_result = self.select_random_result()
        self.get_streaming_services_urls()
        #self.write_to_db()

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
        ''' call the YouTube Music API and return a list of results '''
        song_search_results = self.ytmusic.search(self.search_string, "songs", limit=200)

        #print(song_search_results[0])

        results_list = []
        for song in song_search_results:
            results_list.append([song["artists"][0]["name"] + " - " + song["title"],
                                 song["thumbnails"][-1]["url"],
                                 song["videoId"]])
        
        return results_list

    def select_random_result(self):
        ''' select a random artist from the api response data. if no data is available
            then the api is called again until data exists to choose from '''
        api_data = []
        while len(api_data) == 0:
            api_data = self.call_YT_API()

        # Choose an artist from the list
        random_selection = api_data[randint(0,len(api_data) - 1)]
        # Build and append the YTMusic URL
        random_selection.append(f"https://music.youtube.com/watch?v={random_selection[2]}")

        # Debug Printing
        #for i in range(0, len(random_selection)):
        #    print(i, "-", random_selection[i])

        return random_selection

    def get_streaming_services_urls(self):
        ''' call song.link API to get all other major streaming services URLs
            AND a better thumbnail image than the YTMusic one...
            1. Spotify = BEST
            2. Amazon Music
            3. YTMusic = WORST (default if no other results are available) '''
        url = "https://api.song.link/v1-alpha.1/links"
        params = {
            "url": self.random_result[3],
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
            {"key": "boomplay", "label": "Boomplay", "icon": "boomplay.svg"},
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
            thumbnail = self.random_result[1]

        self.random_result.append({"links": links, "thumbnail": thumbnail})

    def write_to_db(self):
        ''' write the new artist data to the database for the website to use '''
        conn = sqlite3.connect(self.DB_PATH)
        cur = conn.cursor()

        # Insert the artist data
        cur.execute("INSERT INTO random_artists (name, img_url, url) VALUES (?, ?, ?)", (self.random_result[0], self.random_result[1], self.random_result[2]))

        conn.commit()
        conn.close()


if __name__ == "__main__":
    app = RandomGenerator()

