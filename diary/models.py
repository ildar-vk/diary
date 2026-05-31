import pymorphy3
from django.db import models
from django.conf import settings
from django.utils import timezone

morph = pymorphy3.MorphAnalyzer()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    keywords = models.TextField(
        verbose_name='Ключевые слова',
        help_text='Через запятую, например: спорт, бег, зарядка'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Entry(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    entry_date = models.DateField(
        default=timezone.now,
        verbose_name='Дата записи'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entries',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title

    def auto_assign_category(self):
        """Автоматически назначает категорию по ключевым словам с лемматизацией."""
        if not self.content and not self.title:
            return

        text = f"{self.title} {self.content}"
        words = [
            w.strip('.,!?()"/\\:;[]{}').lower()
            for w in text.split()
        ]
        lemmatized_words = [
            morph.parse(w)[0].normal_form for w in words if w
        ]

        for cat in Category.objects.all():
            keywords = [
                kw.strip().lower()
                for kw in cat.keywords.split(',')
                if kw.strip()
            ]
            if any(kw in lemmatized_words for kw in keywords):
                self.category = cat
                return

    def save(self, *args, **kwargs):
        if not self.category:
            self.auto_assign_category()
        super().save(*args, **kwargs)
