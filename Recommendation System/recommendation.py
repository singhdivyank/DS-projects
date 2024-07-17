import pandas as pd
import itertools

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from typing import Union


class Recommendation:
    def __init__(self, file_name: str) -> None:
        self.df = pd.read_csv(filepath_or_buffer=file_name, index_col=0)
        self.vectorizer = TfidfVectorizer(analyzer='word')

    def compute_similarity(self, matrix, id: int) -> list:
        cosine_similarity = linear_kernel(X=matrix, Y=matrix)
        similarity_score = list(enumerate(cosine_similarity[id]))
        # sort in reverse
        similarity_score = sorted(similarity_score, key=lambda x:x[1], reverse=True)
        similarity_score = [list(group) for val, group in itertools.groupby(similarity_score, lambda x:x[1]>=0.2) if val]
        return similarity_score[0]

    def get_choices(self, title: str):
        df = self.df[self.df['Title'] == title]
        user_choice = {
            'title': title, 
            'authors': df['Authors'].to_list(),
            'index': df.index.values.astype(dtype=int)[0]
        }
        return user_choice

    def get_recommendations(self, recommendations: list) -> Union[list, list]:
        
        titles, summaries = [], []
        
        for recommendation in recommendations:
            for title, _ in recommendation.items():
                summary = self.df[self.df['Title'] == title]['Summary'].values[0]
                if title not in titles:
                    titles.append(title)
                if summary not in summaries:
                    summaries.append(summary)
        
        return titles, summaries
    
    def make_recommendation(self, choices: dict) -> Union[list, list]:
        recommendations = []
        
        # normalization
        title_tfidf_matrix = self.vectorizer.fit_transform(raw_documents=self.df['Title'])
        authors_tfidf_matrix = self.vectorizer.fit_transform(raw_documents=choices.get('authors'))
        
        # cosine similarity
        title_score = self.compute_similarity(matrix=title_tfidf_matrix, id=choices.get('index'))
        print("title_score: ", title_score)
        author_score = self.compute_similarity(matrix=authors_tfidf_matrix, id=choices.get('index'))
        print("author_score: ", author_score)

        # all relavant titles
        for idx in title_score:
            if not self.df['Title'].iloc[idx[0]] == choices.get('title'):
                recommendations.append({self.df['Title'].iloc[idx[0]]: idx[1]})
        # all relavant authors
        for idx in author_score:
            if not self.df['Title'].iloc[idx[0]] in recommendations and not self.df['Title'].iloc[idx[0]] == choices.get('title'):
                recommendations.append({self.df['Title'].iloc[idx[0]]: idx[1]})
        # sort all recommendations in descending order
        recommendations = sorted(recommendations, key=lambda x:list(x.values())[0], reverse=True)
        
        # get titles and summaries
        titles, summaries = self.get_recommendations(recommendations=recommendations)
        return titles, summaries
    