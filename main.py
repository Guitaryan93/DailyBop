# Main program for updating the DailyBop Neocities site data

from pathlib import Path
import sqlite3
from jinja2 import Environment, FileSystemLoader


class App:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.DB_PATH = self.BASE_DIR/"database"/"database.db"
        self.TEMPLATES_PATH = self.BASE_DIR/"templates"
        self.artist = self.get_artist_data()
        self.build_HTML()
        
    def get_artist_data(self):
        ''' pull the latest artists data from the db '''
        # connect to the db
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row  # Allow access via column name (like Python dict)
        cursor = conn.cursor()

        # Query the data and return a list
        cursor.execute("SELECT * FROM random_artists ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()

        # Wrap the row into a dictionary
        artist_dict = dict(row)

        # Close the DB connection
        conn.close()

        return artist_dict

    def build_HTML(self):
        ''' build the HTML file using the artist data '''
        env = Environment(loader=FileSystemLoader(self.TEMPLATES_PATH))
        template = env.get_template("index_template.html")

        html_output = template.render(artist=self.artist)

        # Save HTML output
        with open(self.BASE_DIR/"index.html", "w", encoding="utf-8") as f:
            f.write(html_output)


if __name__ == "__main__":
    app = App()
