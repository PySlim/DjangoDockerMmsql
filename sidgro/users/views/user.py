"""User ViewSets"""
import requests
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


from sidgro.users.models import User
from sidgro.users.serializers.user import UserModelSerializer


#Vista Model
class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.filter(active=True)
    serializer_class = UserModelSerializer


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active=False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

