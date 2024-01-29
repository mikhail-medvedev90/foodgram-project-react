"""Models with custom user model and subscription model."""
from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import DEFAULT_NAME_LENGTH


class User(AbstractUser):
    """Custom user model."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    first_name = models.CharField('first name', max_length=DEFAULT_NAME_LENGTH)
    last_name = models.CharField('last name', max_length=DEFAULT_NAME_LENGTH)

    email = models.EmailField(
        "email address",
        unique=True,
    )

    class Meta:
        """
        Set verbose name and verbose name plural.

        Defaults to ordering by id.
        """

        ordering = ('first_name', 'last_name',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        """Return a string representation of User object."""
        return self.username


class Subscribe(models.Model):
    """Subscription model."""

    user = models.ForeignKey(
        User,
        related_name='subscribe',
        verbose_name='Subscriber',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        verbose_name='Author',
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
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self) -> str:
        """Return a string representation of subscription information."""
        return (
            f'{self.user} {"subscribed on"} {self.author}'
        )
