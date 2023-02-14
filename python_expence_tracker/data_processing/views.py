from select import select
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from .actions import *
from .utils import responce_util


# Create your views here.
@permission_classes((IsAuthenticated,))
class UploadData(APIView):
    actions = {}
    action = ''

    def post(self, request, *args, **kwargs):
        self.actions = PostUpdateAction
        self.action = self.kwargs.get('action','')
    
        if self.action not in self.actions.keys():
            return responce_util(s)