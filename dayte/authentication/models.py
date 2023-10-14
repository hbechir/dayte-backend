from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Code(models.Model):
    code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()  # Set created_at if it's not already set
        if not self.expiration_time:
            self.expiration_time = self.created_at + timezone.timedelta(minutes=5)
        super(Code, self).save(*args, **kwargs)

    def is_expired(self):
        now = timezone.now()
        return now > self.expiration_time
