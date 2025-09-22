#! /bin/bash

# Setup venv
cd $HOME/DailyBopProject
source venv/bin/activate

# Get the random artist and add it to the database
python3 $HOME/DailyBopProject/scripts/youtube_randomizer.py

# Build the HTML page for the website
python3 $HOME/DailyBopProject/main.py

# Upload the new HTML to Neocities
$HOME/DailyBopProject/scripts/upload.sh

# Close venv
deactivate
