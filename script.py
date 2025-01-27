from openai import OpenAI
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

client = OpenAI(api_key="<INSERT KEY HERE>")

client_id = "<INSERT KEY HERE>"
client_secret = "<INSERT KEY HERE>"
redirect_uri = "<INSERT URL HERE>"
scope = "user-read-recently-played playlist-read-private"

sp_oauth = SpotifyOAuth(
  client_id = client_id, 
  client_secret = client_secret, 
  redirect_uri = redirect_uri, 
  scope = scope, 
  show_dialog = True
)

sp = Spotify(auth_manager = sp_oauth)

def get_recently_played_songs():
    try:
        results = sp.current_user_recently_played(limit=5)
    except Exception as e:
        print(f"Error fetching recently played songs: {e}")
        return None
    stringed_results = ""
    for i, item in enumerate(results['items']):
        track = item['track']
        stringed_results += (f"{i+1}. '{track['name']}' by {track['artists'][0]['name']}")
    return stringed_results


def generate_prompt(recent_tracks):
  prompt_template = ("I am developing an app that takes in spotify's metadata from a user and\n" 
  "reccomends 5 songs for each of the user's top 5 current favorite songs. I am going to give\n" 
  "you the top 5 songs in a specific format as follows:\n"
  "1. 'Song Name' by Artist Name\n" 
  "2. 'Song Name' by Artist Name\n" 
  "3. 'Song Name' by Artist Name\n" 
  "4. 'Song Name' by Artist Name\n" 
  "5. 'Song Name' by Artist Name\n" 
  "I want you to generate a list of 5 similar songs that the user might like based on the given\n" 
  "songs. I would like you to follow the above template when returning so. Additionally, it is\n" 
  "imperative that the songs are accessible on Spotify as previously, you've recommended songs\n." 
  "that don't exist. Before suggesting a song, please find the song on youtube. Do not explain\n"
  "your results and simply respond with the songs in the format with new lines. Here are the\n"
  "top 5 songs:\n")

  prompt_template += recent_tracks

  return prompt_template


def generate_response(prompt):
  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ])
  return completion.choices[0].message.content


def main():
    songs = get_recently_played_songs()
    prompt = generate_prompt(songs) 
    response = generate_response(prompt)
    print(response)
  

if __name__ == "__main__":
  main()
