from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class Issue(models.Model):
    summary = models.CharField(max_length=200, verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Полное описание', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Статус')
    issue_type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.summary