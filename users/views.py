from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class IndexView(View):
    def get(self, request):
        return HttpResponse(request, "Welcome User")

