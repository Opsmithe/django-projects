from django.core.management.base import BaseCommand
from django.utils.text import slugify
from club.models import Names

class Command(BaseCommand):
    help = 'Generate slugs for existing Names records'

    def handle(self, *args, **options):
        names_without_slugs = Names.objects.filter(slug='')
        for name in names_without_slugs:
            base_slug = slugify(f"{name.firstname}-{name.lastname}-{name.city}")
            slug = base_slug
            counter = 1
            while Names.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            name.slug = slug
            name.save()
            self.stdout.write(f"Generated slug '{slug}' for {name}")
        self.stdout.write(self.style.SUCCESS(f'Successfully generated slugs for {names_without_slugs.count()} records'))
