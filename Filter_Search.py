import streamlit as st
import pandas as pd
import os





if "database_generator" not in st.session_state:
        if os.path.exists('saved_database.csv'):
            st.session_state.database_generator = pd.read_csv('saved_database.csv')

            st.session_state.database_generator["Do you own it?"] = (
            st.session_state.database_generator["Do you own it?"].astype(str).str.lower().map({"true": True, "false": False})
            )
        else:
            st.session_state.database_generator = pd.DataFrame(
                columns=["Game", "Platform", "Do you own it?", "Category"]
            )
if os.path.exists('saved_database.csv'):
    game_database = pd.read_csv('saved_database.csv')
else:
    st.error("Database file not found. Please fill out at least one entry on homepage.")
    quit() #st.stop() is an option as well


st.title(':blue[Filter] Search :video_game:')


def filter_games(game_database, filter_select):
    if filter_select == 'Playing':
        st.header('Playing', divider="blue")
        for index, row in game_database.iterrows():
            if row["Category"].strip().lower() == 'playing':
                #st.subheader(f'{row['Game']}')
                st.page_link(f'https://rawg.io/games/persona-5-royal', label=row['Game'])
                st.write(f'Platform: {row['Platform']}')
                if row['Do you own it?'] == True:
                    st.write('Owned: Yes')
                else:
                    st.write('Owned: No')
                st.write('------------------------')
    elif filter_select == 'Plan To Play':
        st.subheader('Plan To Play')
        for index, row in game_database.iterrows():
            if row["Category"].strip().lower() == 'plan to play':
                st.subheader(f'{row['Game']}')
                st.write(f'Platform: {row['Platform']}')
                if row['Do you own it?'] == True:
                    st.write('Owned: Yes')
                else:
                    st.write('Owned: No')
                st.write('------------------------')
    elif filter_select == 'Completed':
        st.subheader('Completed')
        for index, row in game_database.iterrows():
            if row["Category"].strip().lower() == 'completed':
                st.subheader(f'{row['Game']}')
                st.write(f'Platform: {row['Platform']}')
                if row['Do you own it?'] == True:
                    st.write('Owned: Yes')
                else:
                    st.write('Owned: No')
                st.write('------------------------')
    elif filter_select == 'Dropped':
        st.subheader('Dropped')
        for index, row in game_database.iterrows():
            if row["Category"].strip().lower() == 'dropped':
                st.subheader(f'{row['Game']}')
                st.write(f'Platform: {row['Platform']}')
                if row['Do you own it?'] == True:
                    st.write('Owned: Yes')
                else:
                    st.write('Owned: No')
                st.write('------------------------')


def __main__():
    filter_options = 'Playing', 'Plan To Play', 'Completed', 'Dropped'
    filter_select = st.selectbox('Select a filter option:', filter_options)
    filter_games(game_database, filter_select)

if __name__ == '__main__':
    __main__()