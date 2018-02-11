from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from library.models import Author

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
        if created and not kwargs.get('raw', False):
            Profile.objects.create(user=instance)
        instance.profile.save()


class Newsletter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'newsletter'
        unique_together = (('user', 'author'),)
