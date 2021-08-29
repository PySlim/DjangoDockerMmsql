"""Permissions Model"""
from django.db import models

from sidgro.utils.models import SidgroModel

class Keys(SidgroModel):
    id_key = models.AutoField(primary_key=True)
    operation_id = models.IntegerField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta(SidgroModel.Meta):
        db_table ="Key"
        verbose_name_plural = "Keys"

    def __str__(self):
        return "id: {}".format(self.id_key)