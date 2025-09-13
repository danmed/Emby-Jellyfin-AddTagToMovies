# jelly-tagmovies.py

import requests
import json

# --- JELLYFIN CONFIGURATION ---
JELLYFIN_SERVER_URL = "http://YOUR_JELLYFIN_IP:8096"
JELLYFIN_API_KEY = "YOUR_JELLYFIN_API_KEY_HERE"
JELLYFIN_USER_ID = "YOUR_JELLYFIN_USER_ID_HERE"
TAG_TO_ADD = "YOUR_TAG"
# ------------------------------------------

# Set up the headers for the API requests
headers = {
    'X-Emby-Token': JELLYFIN_API_KEY,
    'Content-Type': 'application/json',
}

def add_tag_to_all_movies():
    """
    Fetches all movies on a Jellyfin server and adds a global tag
    to the simple 'Tags' array.
    """
    print("Starting Jellyfin script: Add Global Tag")

    # 1. Get a list of all movie items for the specified user
    try:
        get_movies_url = f"{JELLYFIN_SERVER_URL}/Users/{JELLYFIN_USER_ID}/Items?Recursive=true&IncludeItemTypes=Movie"
        response = requests.get(get_movies_url, headers=headers)
        response.raise_for_status()
        movies = response.json().get('Items', [])
        print(f"Found {len(movies)} movies in the library.")
    except requests.exceptions.RequestException as e:
        print(f"FATAL ERROR: Could not fetch movie list. Check URL, API Key, and User ID. Details: {e}")
        return

    movies_updated = 0
    movies_failed = 0
    # 2. Loop through each movie to get its full data and update it
    for movie in movies:
        movie_id = movie['Id']
        movie_name = movie['Name']

        try:
            # Get the full data for the movie item
            get_item_url = f"{JELLYFIN_SERVER_URL}/Users/{JELLYFIN_USER_ID}/Items/{movie_id}"
            item_response = requests.get(get_item_url, headers=headers)
            item_response.raise_for_status()
            item_data = item_response.json()
            
            # Use the simple 'Tags' field for Jellyfin
            current_tags = item_data.get('Tags', [])
            
            if TAG_TO_ADD not in current_tags:
                print(f"Updating '{movie_name}' (ID: {movie_id}). Adding tag...")
                
                # Add the new tag directly to the list
                current_tags.append(TAG_TO_ADD)
                item_data['Tags'] = current_tags

                # POST the entire updated item back to the server
                update_url = f"{JELLYFIN_SERVER_URL}/Items/{movie_id}"
                post_response = requests.post(update_url, headers=headers, data=json.dumps(item_data))
                post_response.raise_for_status()

                print(f"    -> Success. Server responded with status {post_response.status_code}.")
                movies_updated += 1
            
        except requests.exceptions.RequestException as e:
            print(f"  - FAILED to process '{movie_name}'. Error: {e}")
            movies_failed += 1

    print("\n--- Script Finished ---")
    print(f"Successfully updated {movies_updated} movies.")
    if movies_failed > 0:
        print(f"Failed to update {movies_failed} movies. Check logs above.")
    else:
        print("All movies processed successfully.")


if __name__ == "__main__":
    add_tag_to_all_movies()
