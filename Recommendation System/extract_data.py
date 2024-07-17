import pandas as pd

from langchain_community.document_loaders import ArxivLoader

# TODO- convert this to API
def get_data(query: str, csv_file: str) -> None:

    """
    load research papers from ARXIV using LangChain dataloader
    and save the results in a CSV file for recommendations

    Params:
        query (str): search query related to the papers' content
        csv_file (str): name of CSV file
    """

    extracted_data = []
    # get contents using LangChain data loader
    ARXIV_data = ArxivLoader(
        query=query, 
        load_max_docs=10
    ).load()

    # get all data as a list
    for idx, data in enumerate(ARXIV_data):
        metadata, content = data.metadata, data.page_content
        extracted_data.append({
            "S. No.": idx + 1,
            "Title": metadata.get('Title'),
            "Authors": metadata.get('Authors'),
            "Summary": metadata.get('Summary'),
            "Content": content
        })
    # convert to DataFrame
    final_data = pd.DataFrame(data=extracted_data)
    # save as csv
    final_data.to_csv(path_or_buf=csv_file)
    