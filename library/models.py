from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    born_at = models.DateField()
    died_at = models.DateField()
    contact = models.CharField(max_length=11)
    bio = models.TextField(max_length=200)
    picture = models.ImageField(upload_to='author_images/', blank=True, null=True)

    class Meta:
        db_table = 'Author'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'Country'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    published_at = models.DateField()
    summary = models.TextField(max_length=200)
    link = models.URLField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    Category = models.ManyToManyField(Category)
    picture = models.ImageField(upload_to='book_images/', blank=True, null=True)

    class Meta:
        db_table = 'Book'

    def __str__(self):
        return self.name
