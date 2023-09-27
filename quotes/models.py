from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=100, null=False)
    born_date = models.DateField(null=True, blank=True)
    born_location = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Quote(models.Model):
    quote = models.TextField(max_length=300, null=False)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.fullname}: {self.quote[:20]}{' ...' if len(self.quote) > 20 else ''}"



