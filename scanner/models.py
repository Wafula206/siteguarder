from django.db import models
from django.conf import settings

class ScanResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='scan_results'
    )
    url = models.URLField()
    scan_time = models.DateTimeField(auto_now_add=True)
    is_https = models.BooleanField()
    missing_headers = models.TextField()
    all_headers = models.JSONField()

    def __str__(self):
        return f"{self.url} @ {self.scan_time}"