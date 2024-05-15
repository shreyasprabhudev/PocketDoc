from django.core.management.base import BaseCommand
from website.update_arxiv_papers import main

class Command(BaseCommand):
    help = 'Fetches the latest health papers from arXiv and updates Pinecone'

    def handle(self, *args, **kwargs):
        main()
