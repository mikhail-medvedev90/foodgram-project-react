"""Models with custom user model and subscription model."""
from django.contrib.auth.models import AbstractUser
from django.db import models

DEFAULT_NAME_LENGTH = 150
EMAIL_LENGTH = 254


class User(AbstractUser):
    """Custom user model."""

    first_name = models.CharField('first name', max_length=DEFAULT_NAME_LENGTH)
    last_name = models.CharField('last name', max_length=DEFAULT_NAME_LENGTH)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    email = models.EmailField(
        "email address",
        max_length=EMAIL_LENGTH,
        unique=True,
    )

    class Meta:
        """
        Set verbose name and verbose name plural.

        Defaults to ordering by id.
        """

        ordering = ('id',)
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
