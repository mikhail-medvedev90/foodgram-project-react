"""Models with custom user model and subscription model."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model."""

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    email = models.EmailField(
        _("email address"),
        max_length=254,
        unique=True,
    )

    class Meta:
        """
        Set verbose name and verbose name plural.

        Defaults to ordering by id.
        """

        ordering = ('id',)
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        """Return a string representation of username."""
        return self.username


class Subscribe(models.Model):
    """Subscription model."""

    user = models.ForeignKey(
        User,
        related_name='subscribe',
        verbose_name=_('Subscriber'),
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        verbose_name=_('Author'),
        on_delete=models.CASCADE,
    )

    class Meta:
        """Add unique and check constraints to the subscription model."""

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follower'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='check_not_self_follow',
            ),
        )
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self) -> str:
        """Return a string representation of subscription information."""
        return (
            f'{self.user} {_("subscribed on")} {self.author}'
        )
