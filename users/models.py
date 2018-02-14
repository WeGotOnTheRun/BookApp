from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from library.models import Author,Book,Category


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='user_images/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'profile'

    def __str__(self):
        return '{} {}'.format(self.picture, self.birth_date)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

class favourite_books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)

class FavouriteCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

class RateBook(models.Model):
    """docstring for ClassName"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    rates= (
        (1,  'very Bad'),
        (2,  'Bad'),
        (3,  'Good'),
        (4,  'very Good'),
        (5,  'Excellent'),
      )
    rate = models.IntegerField(choices=rates)


class ReadBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)

class Newsletter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'newsletter'
        unique_together = (('user', 'author'),)
