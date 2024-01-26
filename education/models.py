from django.db import models
from django.conf import settings

from users.models import User


class Course(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=100, verbose_name='название')
    picture = models.ImageField(upload_to='education/', verbose_name='превью',
                                null=True, blank=True)
    description = models.TextField(verbose_name='описание')
    link_course = models.CharField(max_length=150, verbose_name='ссылка на '
                                   'курс', default=None)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    objects = models.Manager()

    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True,
                               blank=True)

    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    picture = models.ImageField(upload_to='education/', verbose_name='превью',
                                null=True, blank=True)
    link_video = models.CharField(max_length=150, verbose_name='ссылка на '
                                                               'видео')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    objects = models.Manager()

    PAYMENT_CHOICES = [
        ('наличными', 'cash'),
        ('перевод на счет', 'transfer to account'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)
    date_of_payment = models.DateTimeField(verbose_name='день оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE,
                                    verbose_name='оплаченный курс',
                                    null=True, blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                                    verbose_name='оплаченный урок',
                                    null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=3,
                                         verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES,
                                      verbose_name='способ оплаты')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'
