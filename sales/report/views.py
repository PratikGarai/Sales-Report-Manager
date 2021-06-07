from django.shortcuts import render
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_img
from .models import Report

def create_report_view(request):
    if request.is_ajax() :
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        img = get_report_img(image)
        author = Profile.objects.get(user=request.user)

        Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({
            'message' : 'success'
        })
    
    return JsonResponse({})