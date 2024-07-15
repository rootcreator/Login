from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    employment_status = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    state_of_origin = models.CharField(max_length=50, blank=True)
    local_government_area = models.CharField(max_length=50, blank=True)
    highest_education_level = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=20, blank=True)
    work_email = models.EmailField(blank=True)
    work_id_card = models.ImageField(upload_to='work_id_cards/', blank=True)
    government_issued_id = models.ImageField(upload_to='government_ids/', blank=True)
    work_place = models.CharField(max_length=255, blank=True)
    course_of_expertise = models.CharField(max_length=255, blank=True)
    government_id = models.FileField(upload_to='government_ids/', blank=True)

    def __str__(self):
        return self.user.username
