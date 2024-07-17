import pandas as pd
import streamlit as st

from extract_data import get_data
from recommendation import Recommendation

FILE_NAMES = {
    'LLM': 'llm.csv'
}

# get_data(query=user_query, csv_file=file_name)

def recommend_papers(file_name: str, user_choice: str):
    rec_ob = Recommendation(file_name=file_name)
    choice_dict = rec_ob.get_choices(title=user_choice)
    print(choice_dict)
    rec_title, rec_summary = rec_ob.make_recommendation(choices=choice_dict)
    # render on UI
    cols = st.columns(len(rec_title))
    for i in range(0, len(rec_title)):
        cols[i].text_area(
            label="Paper Title",
            value=rec_title[i],
            key=f"Titles_{i}"
        )
    for i in range(0, len(rec_summary)):
        cols[i].text_area(
            label="Paper Summary",
            value=rec_summary[i],
            key=f"Summaries_{i}"
        )

st.title(body='Jhakaas Newsvala')

if 'topic' not in st.session_state:
    st.session_state['topic'] = None
if 'title' not in st.session_state:
    st.session_state['title'] = None

# get choice of topic from user
topic = st.selectbox(
    label='Choose topic', 
    options=['LLM', 'Machine Learning'], 
    label_visibility="visible"
)

if st.button(label='Continue', key='Topic selection'):
    st.session_state['topic'] = topic

if st.session_state['topic']:
    file_name = FILE_NAMES.get(st.session_state['topic'])
    print(file_name)
    df = pd.read_csv(filepath_or_buffer=file_name, index_col=0)
    print(df['Title'].head())

    title = st.selectbox(
        label='Choose your paper',
        options=df['Title'].to_list(),
        label_visibility="visible"
    )
    if st.button(label='Choose', key='Title selection'):
        st.session_state['title'] = title

if st.session_state['title']:
    print(st.session_state['title'])
    summary = df[df['Title'] == st.session_state['title']]['Summary'].values[0]
    print(summary)
    # render paper summary and a button on the UI
    st.text_area(
        label="Paper Summary", 
        value=summary,
        key="Show summary"
    )
    if st.button('Recommend Papers', key='Paper selection'):
        print(st.session_state['title'])
        # run recommendation algorithm
        with st.spinner(text='Loading your recommendations'):
            recommend_papers(file_name=file_name, user_choice=st.session_state['title'])
