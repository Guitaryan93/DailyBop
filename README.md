# 🎶 Daily Bop

**Daily Bop** is a simple web app that helps you **discover new music every day**—outside of the algorithms.
Each day, the site randomly selects a music artist and shares links to listen across all major streaming platforms.

---

## 🌟 Features

* 🎲 **Daily Random Artist** – A new artist is surfaced every 24 hours to encourage music exploration.
* 🔗 **Multi-Platform Links** – Uses the **Songlink API** to provide one-click access to the same track/artist on:

  * Spotify
  * Apple Music
  * YouTube Music
  * Amazon Music
  * Deezer
  * …and more!
* 🐍 **Automated Backend** – A Python script fetches a random artist using **YouTube Music’s API**, then retrieves cross-platform links.

---

## 🚀 How It Works

1. **Random Artist Selection**
   A Python script queries YouTube Music’s API to select a random artist.
2. **Cross-Platform Link Gathering**
   The script calls the **Songlink API** to gather matching links for other major streaming services.
3. **Daily Update**
   The site refreshes daily to feature a brand-new artist.

---

## 🛠️ Tech Stack

* **Python** – backend scripting and API calls
* **YouTube Music API** – random artist selection
* **Songlink API** – cross-platform streaming links
* **HTML/CSS/JS and Jinja2** – building static frontend using templating logic

---

## ⚡ Getting Started (Development)

1. **Clone the repo**

   ```bash
   git clone https://github.com/
   cd daily-bop
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup SQLite Database**

   ```bash
   mkdir database
   touch database/database.db
   ```

4. **Run the YouTube Music Randomizer script**
   This will fetch an artist and add them to the `random_artists` database table.

   ```bash
   python3 scripts/youtube_randomizer.py
   ```

5. **Run the main script**
   This will generate the index.html from the template file. This is then pushed to your web server.

   ```bash
   python3 main.py
   ```
   
---

## 🌍 Live Site

👉 [**Daily Bop**](https://dailybop.neocities.org/)

---

## 🤝 Contributing

Pull requests and feature ideas are welcome!
If you’d like to contribute:

1. Fork the repo
2. Create a new branch (`git checkout -b feature-name`)
3. Commit changes
4. Open a Pull Request

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
