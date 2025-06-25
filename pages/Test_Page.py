import streamlit as st
import pandas as pd
import os
import requests
import json

st.set_page_config(
    page_title='Test Page'
)

def search_game(game_title):
    
    api_key = "8f008a0266694bb29359c20463fc898a"
    url = f"https://api.rawg.io/api/games?search={game_title}&8f008a0266694bb29359c20463fc898a"
    params = {
        "search": game_title,
        "key": api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def game_searcher():
    search_term = st.text_input("Enter the name of the game you are searching for")
    if search_term != "":
        search = search_game(search_term)
        game_name = search["results"][0]["name"] if search and "results" in search and len(search["results"]) > 0 else "Game not found"
        release_date = search['results'][0]['released'] if search and 'results' in search and len(search["results"]) > 0 else "Release date N/A"
        st.write(game_name)
        st.write(release_date)

def __main__():
    result = game_searcher()
    

if __name__ == "__main__":
    __main__()