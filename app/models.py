"""Module models for app."""
from datetime import datetime, timezone

from django.core.exceptions import ValidationError
from django.db import models


TITLE_LENGTH_MAX = 50
DESCRIPTION_LENGTH_MAX = 10000


def get_datetime() -> datetime:
    """
    Get the current datetime in UTC timezone.

    Returns:
        datetime: The current datetime in UTC timezone.
    """
    return datetime.now(timezone.utc)


def check_date_created(dt: datetime) -> None:
    """
    Check if the provided datetime is not in the future.

    Args:
        dt (datetime): The datetime to check.

    Raises:
        ValidationError: If the provided datetime is in the future.
    """
    if dt > get_datetime():
        raise ValidationError(
            'date and time is bigger than current',
            params={'created': dt},
        )


class CreatedMixin(models.Model):
    """
    Mixin class for adding a 'created' field to models.

    Attributes:
        created (DateTimeField): The field representing the creation datetime.
    """

    created = models.DateTimeField(
        ('created'), default=get_datetime,
        null=True, blank=True,
        validators=[check_date_created],
    )

    class Meta:
        """
        Meta options for the CreatedMixin model.

        Attributes:
            abstract (bool): Indicates that this is an abstract base class.
        """

        abstract = True


class Button(CreatedMixin):
    """
    Model class for buttons.

    Attributes:
        id (SmallAutoField): The primary key field.
        title (TextField): The title of the button.
        description (TextField): The description of the button.
        parent_id (ForeignKey): The foreign key referencing the parent button.
    """

    id = models.SmallAutoField(primary_key=True, editable=False)

    title = models.TextField(
        'title', null=False, blank=False, max_length=TITLE_LENGTH_MAX)
    description = models.TextField(
        'description',
        null=True,
        blank=True,
        max_length=DESCRIPTION_LENGTH_MAX,
    )
    parent_id = models.ForeignKey(
        'button', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self) -> str:
        """
        Get the string representation of the button.

        Returns:
            str: The title of the button.
        """
        return self.title

    class Meta:
        """
        Meta options for the Button model.

        Attributes:
            db_table (str): The name of the database table.
            ordering (list): The default ordering for the model instances.
            verbose_name (str): The human-readable name of the model.
            verbose_name_plural (str):
            The human-readable plural name of the model.
        """

        db_table = '"django_db"."button"'
        ordering = ['title', 'description']
        verbose_name = ('button')
        verbose_name_plural = ('buttons')
