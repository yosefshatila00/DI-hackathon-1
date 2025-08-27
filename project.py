import base64
import json
import requests
import random
from textblob import TextBlob



client_id = "4f562007e3534dcd9a00bd282a135f4d"
client_secret = "8420120be74c41149f49502bd3f18761"



def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes =auth_string.encode("utf-8")
    auth_base64=str(base64.b64encode(auth_bytes),"utf-8")
 
    url = "https://accounts.spotify.com/api/token"
    headers={"Authorization":"Basic "+ auth_base64,
             "Content-Type":"application/x-www-form-urlencoded"}
    data={"grant_type":"client_credentials"}
    result = requests.post(url,headers=headers,data=data)
    json_result = json.loads(result.content)
    token= json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_music(token, music_mood):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": music_mood,
        "type": "track",
        "limit": 10}
    result = requests.get(url, headers=headers, params=params)
    json_result = json.loads(result.content)
    tracks = json_result.get("tracks", {}).get("items", [])
    if len(tracks) == 0:
        return None
    return tracks

def get_mood(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity   
    if polarity > 0.2:
        return "happy and energetic"
    elif polarity < -0.2:
        return "sad music" 
    else:
        return "chill and peaceful"
    
def suggest_music(text):
    mood=get_mood(text)
    print(mood)
    token=get_token()
    tracks=search_for_music(token,mood)
    chosen_track=random.choice(tracks)
    return {"title":chosen_track["name"],
            "artist":chosen_track["artists"][0]["name"],
            "url":chosen_track["external_urls"]["spotify"]}

if __name__ == "__main__":

    print("simple music suggester")
    while True:
        user_input = input("How are you feeling? ")
        
        if user_input in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
            
        if user_input.strip():
            result = suggest_music(user_input)
            if result:
                print(f"Recommended: {result['title']} by {result['artist']}")
                print(f"Listen here: {result['url']}")
            else:
                print("Sorry, couldn't find a recommendation. Try again!")
        else:
            print("\n\nPlease enter how you're feeling!")





