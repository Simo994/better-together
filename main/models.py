from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('solved', 'Решена'),
        ('rejected', 'Отклонена'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    image_before = models.ImageField(upload_to='requests/before/', verbose_name='Фото ДО')
    image_after = models.ImageField(upload_to='requests/after/', null=True, blank=True, verbose_name='Фото ПОСЛЕ')
    rejection_reason = models.TextField(null=True, blank=True, verbose_name='Причина отказа')
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
