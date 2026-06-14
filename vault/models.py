from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model


USER = get_user_model()
# тут нужно сделать класс Todo
class Account(models.Model):
    owner = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name="Владелец"
    )
    # site = models.CharField("Сайт", max_length=255)
    task = models.CharField("Дело", max_length=255)
    # login = models.CharField("Логин", max_length=255)
    note = models.CharField("Примечание", max_length=255)
    # password = models.CharField("Пароль", max_length=255)
    importance = models.CharField("Срочность", max_length=255)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    deadline = models.DateTimeField("Дата дедлайна")

    class Meta:
        verbose_name = "Созданное дело"
        verbose_name_plural = "Созданные дела"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.task} ({self.created_at})"

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         old = Account.objects.filter(pk=self.pk).only("password").first()
    #         if old is not None and old.password != self.password:
    #             self.password_changed_at = timezone.now()
    #     else:
    #         if not self.password_changed_at:
    #             self.password_changed_at = timezone.now()
    #
    #     super().save(*args, **kwargs)



