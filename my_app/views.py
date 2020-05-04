from django.shortcuts import render

#Web Scrapping
from bs4 import BeautifulSoup
from urllib.request import urlopen
from requests.compat import quote_plus

amazon_url ='https://www.amazon.com/s?k={sear}&ref=nb_sb_noss_2'
walmart_url = 'https://www.walmart.com/search/?page=1&query={}&sort=price_low'
target_url = 'https://www.target.com/s?searchTerm={sear}'

# Create your views here.
def AppPage(request):

    search = request.POST.get('search')

    final_url = walmart_url.format(quote_plus(search))
    #response = requests.get(final_url)
    #data = response.text

    html = urlopen(final_url)
    soup = BeautifulSoup(html,"lxml")

    #soup = BeautifulSoup(data, features='html.parser')

    output = str(soup.find_all('script', {'id':'searchContent'}))

    total_prod = output.count("productId")

    newlist = output.split("productId")

    walmart_list = []

    for i in range(1,total_prod):

        if ('offerPrice') in newlist[i]:

            if 'title' in newlist[i]:
                walmart_item_title = newlist[i].split('title')[1].split('description')[0].split("productImageUrl")[0].replace("\"","").replace("<mark>","").replace(",","").replace(":","").replace("</mark>","")
            else:
                break

            walmart_item_price = newlist[i].split('offerPrice')[1].split(',')[0].replace("\"","").replace(":","")
            walmart_item_url = str('https://www.walmart.com'+newlist[i].split('productPageUrl')[1].split(',')[0].replace("\"","").replace(":",""))
            if 'sellerName' in newlist[i]:
                walmart_item_seller = newlist[i].split('sellerName')[1].split(',')[0].replace("\"","").replace(":","")
            else:
                walmart_item_seller = 'NA'

            if 'srcSet' in newlist[i]:
                walmart_item_image = newlist[i].split('srcSet')[1].split(',')[0].replace("\"","").lstrip(':')
            elif 'productImageUrl' in newlist[i]:
                walmart_item_image = newlist[i].split('productImageUrl')[1].split(',')[0].replace("\"","").lstrip(':')


            if 'customerRating' in newlist[i]:
                walmart_item_rating= newlist[i].split('customerRating')[1].split(',')[0].replace("\"","").replace(":","")

            else:
                walmart_item_rating = 0

            if 'numReviews' in newlist[i]:
                walmart_item_numberreviews = newlist[i].split('numReviews')[1].split(',')[0].replace("\"","").replace(":","")
            else:
                walmart_item_numberreviews = 0


        elif('minPrice') in newlist[i]:

            if 'title' in newlist[i]:       
                walmart_item_title = newlist[i].split('title')[1].split('description')[0].split("productImageUrl")[0].replace("\"","").replace("<mark>","").replace(",","").replace(":","").replace("</mark>","")
            else:
                break

            walmart_item_price = newlist[i].split('minPrice')[1].split(',')[0].replace("\"","").replace(":","")
            walmart_item_url = str('https://www.walmart.com'+newlist[i].split('productPageUrl')[1].split(',')[0].replace("\"","").replace(":",""))

            if 'sellerName' in newlist[i]:
                walmart_item_seller = newlist[i].split('sellerName')[1].split(',')[0].replace("\"","").replace(":","")
            else:
                walmart_item_seller = 'NA'

            if 'srcSet' in newlist[i]:
                walmart_item_image = newlist[i].split('srcSet')[1].split(',')[0].replace("\"","").lstrip(':')
            elif 'productImageUrl' in newlist[i]:
                walmart_item_image = newlist[i].split('productImageUrl')[1].split(',')[0].replace("\"","").lstrip(':')


            if 'customerRating' in newlist[i]:
                walmart_item_rating= newlist[i].split('customerRating')[1].split(',')[0].replace("\"","").replace(":","")

            else:
                walmart_item_rating = 0

            if 'numReviews' in newlist[i]:
                walmart_item_numberreviews = newlist[i].split('numReviews')[1].split(',')[0].replace("\"","").replace(":","")
            else:
                walmart_item_numberreviews = 0

        walmart_list.append((walmart_item_title,walmart_item_price,walmart_item_url,walmart_item_seller,walmart_item_image,walmart_item_rating,walmart_item_numberreviews))

    return render(request,'my_app/app_name.html',context = {'walmart_list':walmart_list})
