from django.db import models
from django.utils import timezone


class AnatomicalArea(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Modality(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class MLTask(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Dataset(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    external_path = models.CharField(max_length=1000, blank=True, null=True)
    local_path = models.CharField(max_length=500, blank=True, null=True)
    record_count = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    anatomical_area = models.ForeignKey(
        AnatomicalArea, on_delete=models.SET_NULL, null=True
    )
    modalities = models.ManyToManyField(Modality, through="DatasetModality")
    ml_tasks = models.ManyToManyField(MLTask, through="DatasetMLTask")
    tags = models.ManyToManyField(Tag, through="DatasetTag")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class DatasetModality(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    modality = models.ForeignKey(Modality, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("dataset", "modality")


class DatasetMLTask(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    ml_task = models.ForeignKey(MLTask, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("dataset", "ml_task")


class DatasetTag(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("dataset", "tag")
