# Emby & Jellyfin Movie Tagging Script

This repository contains two related Python scripts designed to automatically add a specific tag to all movies in an Emby or Jellyfin library. The scripts connect to the server's API, iterate through the movie library, and add a predefined tag if it's not already present.

While Emby and Jellyfin share a common API heritage, they have diverged in how they handle metadata for tags. This necessitated two distinct versions of the script.

***
## Key Differences Between the Scripts

The sole difference between the `emby_tagmovies.py` and `jelly_tagmovies.py` scripts is the format required to update an item's tags.

| Feature | `emby_tagmovies.py` | `jelly_tagmovies.py` |
| :--- | :--- | :--- |
| **Target Field** | `TagItems` | `Tags` |
| **Data Format** | Requires a list of **Objects**, where each object has a `Name` key. | Requires a simple list of **Strings**. |
| **Example JSON** | `{"TagItems": [{"Name": "MyTag"}]}` | `{"Tags": ["MyTag"]}` |
| **Core Logic** | The script checks for and appends a dictionary (`{'Name': 'MyTag'}`) to the `TagItems` list. | The script checks for and appends a string (`'MyTag'`) to the `Tags` list. |

### Why the Difference?

This distinction arises from a change in the API. Emby uses a more complex, structured object to manage tags, which includes a unique `Id` for each tag. Jellyfin simplified this part of the API to use a straightforward array of strings, making it easier to manage but requiring a different data structure in the update request.

All other functionality, including API authentication, item fetching, and server communication, remains identical between the two scripts.
