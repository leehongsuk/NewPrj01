from django.db import models


# Create your models here.
class Article(models.Model):
    name     = models.CharField(max_length=50)
    title    = models.CharField(max_length=50)
    contents = models.TextField()
    url      = models.URLField()
    email    = models.EmailField()
    cdate    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s(%s) / %s' % (self.name, self.email, self.title)
