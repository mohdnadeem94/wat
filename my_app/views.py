from django.shortcuts import render

# Create your views here.
def AppPage(request):
    return render(request,'app_name.html')
