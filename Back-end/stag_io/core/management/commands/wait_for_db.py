"""
Django Command to check if data base is available
"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to wait db"""
    def handle(self, *args, **options):
        pass