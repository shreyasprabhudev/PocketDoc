from django.conf import settings
from celery import shared_task
from sentence_transformers import SentenceTransformer
import pinecone
import arxivscraper

@shared_task
def fetch_and_index_papers():
    pinecone.init(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT)
    index = pinecone.Index('arxiv-papers')

    model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)

    scraper = arxivscraper.Scraper(
        category=settings.ARXIV_SCRAPER_CATEGORY,
        date_from=settings.ARXIV_SCRAPER_DATE_FROM,
        date_until=settings.ARXIV_SCRAPER_DATE_UNTIL
    )
    output = scraper.scrape()

    for paper in output:
        embedding = model.encode(paper['title'] + " " + paper['summary'])
        index.upsert(vectors=[(paper['id'], embedding)])

    print("Papers fetched and indexed.")
