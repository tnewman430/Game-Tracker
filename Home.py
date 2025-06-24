import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title='Game Tracker',
    page_icon='🎮'
)


st.sidebar.success('Welcome to the Game Tracker!')


st.title(':green[Game] Tracker :video_game:')


def toPlayList():
    # Use session state to persist the waitlist across reruns
    if "waitlist" not in st.session_state:
        st.session_state.waitlist = pd.DataFrame([
            {"Game": "", "Platform": "", "Do you own it?": False}
        ])

    # Initialize database_generator
    if "database_generator" not in st.session_state:
        if os.path.exists('saved_database.csv'):
            st.session_state.database_generator = pd.read_csv('saved_database.csv')

            st.session_state.database_generator["Do you own it?"] = (
            st.session_state.database_generator["Do you own it?"]
            .astype(str)
            .str.lower()
            .map({"true": True, "false": False})
            )
        else:
            st.session_state.database_generator = pd.DataFrame(
                columns=["Game", "Platform", "Do you own it?", "Category"]
            )
    


    waitlist = st.session_state.waitlist

    st.write("Edit your to-play list below:")
    edited_df = st.data_editor(waitlist, num_rows="dynamic", key="waitlist_editor")

    if edited_df is not None:
        st.session_state.waitlist = edited_df

    # Allow user to select a row to finalize
    st.markdown("### Finalize an entry to add it to the database:")
    valid_indices = edited_df[
        (edited_df["Game"].str.strip() != "") &
        (edited_df["Platform"].str.strip() != "")
    ].index.tolist()

    if valid_indices:
        selected_index = st.selectbox("Select a row to submit:", valid_indices, format_func=lambda i: str(edited_df.loc[i, "Game"]) if pd.notnull(edited_df.loc[i, "Game"]) else "N/A")

        selected_row = edited_df.loc[selected_index]

        game_placer = st.radio(
            f"Select category for **{selected_row['Game']}**:",
            ["Plan To Play", "Playing", "Completed", "Dropped"],
            key=f"category_{selected_index}"
        )

        if st.button("Submit Entry", key=f"submit_{selected_index}"):
            new_entry = {
                "Game": selected_row["Game"],
                "Platform": selected_row["Platform"],
                "Do you own it?": selected_row["Do you own it?"],
                "Category": game_placer
            }

            df = st.session_state.database_generator
            mask = (df["Game"] == new_entry["Game"]) & (df["Platform"] == new_entry["Platform"])

            if mask.any():
                st.session_state.database_generator.loc[mask, ["Do you own it?", "Category"]] = (
                    new_entry["Do you own it?"], new_entry["Category"]
                )
                st.success(f"Updated entry for {new_entry['Game']}.")
            else:
                st.session_state.database_generator = pd.concat(
                    [df, pd.DataFrame([new_entry])], ignore_index=True
                )
                st.success(f"Added new entry for {new_entry['Game']}.")

            st.session_state.database_generator.to_csv('saved_database.csv', index=False)
                

    else:
        st.info("Fill out at least the Game and Platform fields to submit an entry.")


    
    st.header("Current Game Database:")
    st.dataframe(st.session_state.database_generator)


def __main__():
    toPlayList()


if __name__ == "__main__":
    __main__()




