from django.shortcuts import render

# Create your views here.
def HomePage(request):
    return render(request,'index.html')

def ThanksPage(request):
    return render(request,'thanks.html')
