from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = 'Loads data'

    def handle(self, *args, **options):

        print('Loading data')

        for row in DictReader(open('static/data/users.csv', encoding='utf8')):
            data = User(id=row['id'], username=row['username'],
                        email=row['email'], role=row['role'],
                        first_name=row['first_name'],
                        last_name=row['last_name'], bio=row['bio'])
            data.save()

        for row in DictReader(open('static/data/category.csv',
                              encoding='utf8')):
            data = Category(id=row['id'], name=row['name'], slug=row['slug'])
            data.save()

        for row in DictReader(open('static/data/genre.csv',
                              encoding='utf8')):
            data = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            data.save()

        for row in DictReader(open('static/data/titles.csv', encoding='utf8')):
            data = Title(id=row['id'], name=row['name'], year=row['year'],
                         category_id=row['category'])
            data.save()

        for row in DictReader(open('static/data/genre_title.csv',
                              encoding='utf8')):
            data = GenreTitle(id=row['id'], title_id=row['title_id'],
                              genre_id=row['genre_id'])
            data.save()

        for row in DictReader(open('static/data/review.csv', encoding="utf8")):
            data = Review(id=row['id'], title_id=row['title_id'],
                          text=row['text'], author_id=row['author'],
                          score=row['score'], pub_date=row['pub_date'])
            data.save()

        for row in DictReader(open('static/data/comments.csv',
                              encoding='utf8')):
            data = Comment(id=row['id'], review_id=row['review_id'],
                           text=row['text'], author_id=row['author'],
                           pub_date=row['pub_date'])
            data.save()
