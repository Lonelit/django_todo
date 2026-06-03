from django.db import models
from django.conf import settings
from django.utils import timezone

class Account(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
        verbose_name="Владелец"
    )
    site = models.CharField("Сайт", max_length=255)
    login = models.CharField("Логин", max_length=255)
    password = models.CharField("Пароль", max_length=255)

    created_at = models.DateTimeField("Дата создания", auto_now=True)
    password_change_at = models.DateTimeField("Дата изменения пароля")

    class Meta:
        verbose_name = "Учетная запись"
        verbose_name_plural = "Учетная запись"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.site} {self.login}"

    def save(self, *args, **kwargs):
        if self.pk:
            old = Account.objects.filter(pk=self.pk).only("password").first()
            if old is not None and old.password != self.password:
                self.password_change_at = timezone.now()
            else:
                if not self.password_change_at:
                    self.password_change_at = timezone.now()
            super().save(*args, **kwargs)





