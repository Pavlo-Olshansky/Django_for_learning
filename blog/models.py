import datetime
from django.utils import timezone
from django.db import models
from django.utils.translation import pgettext
from django.utils.translation import ugettext_lazy as _



class Post_blog(models.Model):
    title = models.CharField(help_text=pgettext('help text for MyThing model',
                                                'This is the help text'),
                             max_length = 140)
    time = models.DateField()
    image = models.ImageField(help_text=_('help text'),
                              upload_to='Imagies_from_site', blank=True, null=True)  # blank - field optional
    body = models.TextField()

    def recent_publication(self):
        return timezone.now().date() >= self.time >= timezone.now().date() - datetime.timedelta(weeks = 1)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.title

class AuthorManager(models.Manager):
    def title_count(self, keyword):
        return self.filter(title__icontains=keyword).count()

class MaleManager(models.Model):
    def get_queryset(self):
        return super(MaleManager, self).get_queryset().filter(sex='M')

class FemaleManager(models.Model):
    def get_queryset(self):
        return super(FemaleManager, self).get_queryset().filter(sex='F')

#  Author.men.all() // women
class Author(models.Model):
    title = models.CharField(max_length=140)
    post = models.ManyToManyField(Post_blog)
    # post_fk = models.ForeignKey(Post_blog)
    objects = AuthorManager()
    sex = models.CharField(max_length=1, choices=(
        ('M', 'Male'),
        ('F', 'Female')
    ))

    men = MaleManager()
    women = FemaleManager()
    def __str__(self):
        return self.title



