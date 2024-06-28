from django.db import models
from channels.models import Channel


# Create your models here.
class Campaign(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.PositiveIntegerField()
    objective = models.TextField()

    def __str__(self):
        return self.channel


class AdSet(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    targeting_details = models.TextField()
    budget = models.PositiveIntegerField()


class Ads(models.Model):
    adset = models.ForeignKey(AdSet, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    creative = models.FileField(upload_to="ADS")
    url = models.URLField()
    is_active = models.BooleanField(default=True)


class PerformanceMetric(models.Model):
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE)
    date = models.DateField()
    impressions = models.PositiveIntegerField()
    clicks = models.PositiveIntegerField()
    conversions = models.PositiveIntegerField()
    spend = models.PositiveIntegerField()
    ctr = models.PositiveIntegerField()
    conversion_rate = models.FloatField()


class AudienceDemographics(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    agerange = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    interest = models.CharField(max_length=100)


class SentimentAnalysis(models.Model):
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE)
    positivementions = models.IntegerField(default=0)
    neutralmentions = models.IntegerField(default=0)
    negativementions = models.IntegerField(default=0)
    analysisdata = models.JSONField(null=True, blank=True)
