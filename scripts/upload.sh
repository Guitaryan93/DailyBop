#! /bin/bash

# Upload the latest index.html file to neocities
curl -u "dailybop:mph9myg@ndp6jnw4JZR" -F "index.html=@$HOME/DailyBopProject/index.html" "https://neocities.org/api/upload"
