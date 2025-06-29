from django.db import models

class ScanResult(models.Model):
    url = models.URLField()
    scan_time = models.DateTimeField(auto_now_add=True)
    is_https = models.BooleanField()
    missing_headers = models.TextField()
    all_headers = models.JSONField()

    def __str__(self):
        return f"{self.url} @ {self.scan_time}"