from django.db import models
from django.urls import reverse
from profiles.models import Profile

class Report(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to="reports", blank=True)
    remarks = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.author.user.username + " " + str(self.created)

    def get_absolute_url(self):
        return reverse('report:detail', kwargs={'pk' : self.pk}  )

    class Meta :
        ordering = ('-created',)