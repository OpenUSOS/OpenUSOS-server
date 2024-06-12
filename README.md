# OpenUSOS-server
## Authors: Oskar Kuliński, Filip Ciebiera, Wieńczysław Włodyga   
This is the code for the server used by the OpenUSOS app: https://github.com/OpenUSOS/OpenUSOS

## How to use
To use, run $python app.py

By default the server will run on port :5000

## Self hosting
If you want to self host the server, feel free to do so.
- purchase or find a free hosting service
- register tokens for univerisites for which you want your app to work, you can find more information about it here https://apps.usos.edu.pl/developers/api/
- create a directory and file tokeny/OpenUSOS_data/tokens.py
- create a token dictionary inside with the following format
  
            university_token={
              "Uniwersytet 1" : {
                "Consumer_key": "Your consumer key for university 1",
                "Consumer_secret": "your consumer key for university 1",
                "url" : "link to USOS api installation of the chosen university"},
              "Uniwersytet 2" : {
                "Consumer_key": "Your consumer key for university 2",
                "Consumer_secret": "your consumer key for university 2",
                "url" : "link to USOS api installation of the chosen university"}
            }
  
- run the server
- follow the rest of the instructions in: https://github.com/OpenUSOS/OpenUSOS#self-hosting

## Making your own server
You can create your own server from scratch if you want to, to not have to change anything in the app itself, follow the specifications in api.md.

Should you have any problems feel free to contact us.
