# Main program for updating the DailyBop Neocities site data

from pathlib import Path
import sqlite3
from jinja2 import Environment, FileSystemLoader


class App:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.DB_PATH = self.BASE_DIR/"database"/"database.db"
        self.TEMPLATES_PATH = self.BASE_DIR/"templates"
        self.artist, self.svg_list = self.get_artist_data()
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

        # Pull the SVG images from the SVG DB Table
        cursor.execute("SELECT service, svg, display_name FROM svgs")
        svg_rows = cursor.fetchall()

        # Close the DB connection
        conn.close()

        # Match up the SVG icons to the streaming service URLs
        streaming_services = []
        for svg_row in svg_rows:
            service = svg_row["service"]
            svg = svg_row["svg"]
            display_name = svg_row["display_name"]

            # The column in the artist_dict should match "service"
            url = artist_dict.get(service)
            if url:
                streaming_services.append({
                    "name": service,
                    "url": url,
                    "svg": svg,
                    "display_name": display_name
                })

        return artist_dict, streaming_services

    def build_HTML(self):
        ''' build the HTML file using the artist data '''
        env = Environment(loader=FileSystemLoader(self.TEMPLATES_PATH))
        template = env.get_template("index_template.html")

        html_output = template.render(artist=self.artist, svg_list=self.svg_list)

        # Save HTML output
        with open(self.BASE_DIR/"index.html", "w", encoding="utf-8") as f:
            f.write(html_output)


if __name__ == "__main__":
    app = App()
