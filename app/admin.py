"""Module for project's admin."""
from django.contrib import admin

from .models import Button


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Button model.

    Displays specific fields in the admin interface and marks
    'created' field as read-only.

    Attributes:
        model (Button): The model associated with this admin.
        list_display (tuple): Fields to display in the admin list view.
        readonly_fields (tuple): Fields marked as
        read-only in the admin interface.
    """

    class Meta:
        """
        Metadata options for the ButtonAdmin class.

        Attributes:
            model (Button): The model associated with this admin.
            list_display (tuple): Fields to display in the admin list view.
            readonly_fields (tuple):
            Fields marked as read-only in the admin interface.
        """
    model = Button
    list_display = (
        'title',
        'description',
        'parent_id',
        'created',
    )
    readonly_fields = ('created',)
