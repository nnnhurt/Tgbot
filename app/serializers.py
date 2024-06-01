"""Module serializers for app."""
from rest_framework import serializers

from .models import Button


class ButtonSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Button model.

    Serializes Button instances and includes nested button data.
    """

    class Meta:
        """
        Meta options for ButtonSerializer.

        Attributes:
            model (Button): The model class to serialize.
            fields (list): The fields to include in the serialization.
        """

        model = Button
        fields = ['id', 'title', 'description', 'buttons']

    buttons = serializers.SerializerMethodField()

    def get_buttons(self, obj):
        """
        Get the child buttons of the current button.

        Args:
            obj (Button): The button instance.

        Returns:
            list: A list of serialized child buttons.
        """
        children = Button.objects.filter(parent_id=obj.id)
        return ButtonSerializer(children, many=True).data
