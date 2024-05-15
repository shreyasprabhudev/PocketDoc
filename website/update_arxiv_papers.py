import os
import openai
import arxiv
from django.conf import settings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def fetch_latest_papers(categories, max_results):
    results = []
    for category in categories:
        print(f"Fetching papers for category: {category}")
        search = arxiv.Search(
            query=f"cat:{category}",
            max_results = max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        category_results = list(search.results())
        results.extend(category_results)
        print(f"Fetched {len(category_results)} papers for category {category}")
    print(f"Total papers fetched: {len(results)}")
    return results

def embed_and_upload_to_pinecone(papers, openai_api_key, pinecone_api_key, index_name):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    documents = []
    for paper in papers:
        combined_text = f"{paper.title}\n{paper.summary}"
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        chunks = text_splitter.split_documents([Document(page_content=combined_text, metadata={"title": paper.title})])
        documents.extend(chunks)

    os.environ["PINECONE_API_KEY"] = pinecone_api_key
    pinecone = PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)
    return pinecone

def main():
    papers = fetch_latest_papers(categories=['q-bio.TO', 'q-bio.NC'], max_results=1000)

    embed_and_upload_to_pinecone(
        papers,
        openai_api_key=settings.OPENAI_API_KEY,
        pinecone_api_key=settings.PINECONE_API_KEY,
        index_name="pocketdoc"
    )

if __name__ == "__main__":
    main()
