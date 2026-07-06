from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from programmes.models import Programme

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='reports')
    report_date = models.DateField()
    report_name = models.CharField(max_length=150)
    satisfaction_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Satisfaction score as a percentage (0-100).',
    )

    def __str__(self):
        return self.report_name
