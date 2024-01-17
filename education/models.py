from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    picture = models.ImageField(upload_to='education/', verbose_name='превью',
                                null=True, blank=True)
    description = models.TextField(verbose_name='описание')
    link_course = models.CharField(max_length=150, verbose_name='ссылка на курс',
                                   default=None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    picture = models.ImageField(upload_to='education/', verbose_name='превью',
                                null=True, blank=True)
    link_video = models.CharField(max_length=150, verbose_name='ссылка на видео')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
