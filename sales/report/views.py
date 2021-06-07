from django.shortcuts import get_object_or_404, render
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_img
from .models import Report
from django.views.generic import ListView, DetailView
from django.template.loader import get_template
from django.http.response import HttpResponse
from xhtml2pdf import pisa


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


class ReportListView(ListView):
    model = Report
    template_name = 'report/main.html'


class ReportDetailView(DetailView):
    model = Report
    template_name = 'report/detail.html'


def render_pdf_view(request, pk):
    template_path = 'report/pdf.html'
    response = HttpResponse(content_type='application/pdf')
    obj = get_object_or_404(Report, pk=pk)
    context = {'object' : obj}


    # if download
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # if display
    # response['Content-Disposition'] = 'filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response
    )
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response