from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Bienvenido al asignador de cuadrillas!")
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

def home(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        uploaded_file_url = fs.url(filename)
        return HttpResponse("Archivo cargado correctamente: " + uploaded_file_url)
    return render(request, 'home.html')

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'asignador_web/home.html')

def subir_excel(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        fs = FileSystemStorage(location='ordenes/')
        nombre_archivo = fs.save(archivo.name, archivo)
        return render(request, 'asignador_web/exito.html', {'archivo': nombre_archivo})
    return render(request, 'asignador_web/subir_excel.html')
