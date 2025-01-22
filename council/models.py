# ... (diğer importlar sabit kalabilir)
from django.db import models
from django.conf import settings

# models.py'da Way modeliniz zaten şu şekilde revize edilmiş olsun (daha önce konuştuğumuz gibi):


class Way(models.Model):
    base_type = models.CharField(max_length=50)
    way_id = models.IntegerField(unique=True)
    nodes = models.JSONField()
    destination = models.CharField(max_length=255, null=True, blank=True)
    highway = models.CharField(max_length=50)
    hist_ref = models.CharField(max_length=50, null=True, blank=True)
    loc_name = models.CharField(max_length=50, null=True, blank=True)
    maxspeed = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=255)
    oneway = models.CharField(max_length=10)
    ref = models.CharField(max_length=50)
    lanes = models.CharField(max_length=10, null=True, blank=True)
    nat_ref = models.CharField(max_length=50, null=True, blank=True)
    toll = models.CharField(max_length=10, null=True, blank=True)
    tracker_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


# Department modeline dokunmuyoruz.


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="council_departments", null=True, blank=True
    )
