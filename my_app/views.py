from django.shortcuts import render


amazon_url ='https://www.amazon.com/s?k={sear}&ref=nb_sb_noss_2'
walmart_url = 'https://www.walmart.com/search/?query={sear}'
target_url = 'https://www.target.com/s?searchTerm={sear}'

# Create your views here.
def AppPage(request):
    return render(request,'app_name.html')
