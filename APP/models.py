from django.db import models

# Create your models here.


class People(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.BigIntegerField(primary_key=True)
    gender = models.CharField(max_length=50)
    email_id = models.EmailField()
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "People"
