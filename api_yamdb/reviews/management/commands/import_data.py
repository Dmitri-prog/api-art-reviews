from csv import DictReader
from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import MyUser

MODEL_CSV = {
    'users.csv': MyUser,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': Title.genre.through,
    'review.csv': Review,
    'comments.csv': Comment,
}


class Command(BaseCommand):

    help = 'Импорт данных из csv файлов'

    def handle(self, *args, **options):
        for csv, model in MODEL_CSV.items():
            model.objects.all().delete()
            with open(f'{settings.BASE_DIR}/static/data/{csv}',
                      'r', encoding='utf-8') as csv_file:
                reader = DictReader(csv_file)
                for row in reader:
                    if 'category' in row:
                        row['category_id'] = row['category']
                        del row['category']
                    if 'author' in row:
                        row['author_id'] = row['author']
                        del row['author']
                    model.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS('Загрузка выполнена'))
