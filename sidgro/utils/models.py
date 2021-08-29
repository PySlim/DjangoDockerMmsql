"""Django Models Utilities"""

from django.db import models

class SidgroModel(models.Model):
    """Modelo utilitario del proyecto registra fecha y hora de creacion
        asi como hora y fecha de ultima actualización.
    """
    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created',
        null=True
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified',
        null=True
    )

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created','-modified']