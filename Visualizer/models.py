from django.db import models

# Create your models here.
class LottoType(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    nums = models.IntegerField()
    special_nums = models.IntegerField(null=True, blank=True)
    has_special = models.BooleanField()

    def __str__(self):
        return self.name

class LottoDraw(models.Model):
    lotto_number = models.CharField(max_length=128)
    lotto_date = models.DateField()
    lotto_type = models.ForeignKey(LottoType, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lotto_date', 'lotto_type'], name='unique_lotto_date_lotto_type')
        ]
    def __str__(self):
        return self.lotto_date.strftime('%Y/%m/%d') + " " + self.lotto_type.name

