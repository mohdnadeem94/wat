from django.shortcuts import render

#Web Scrapping
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
#&sort=price_low
amazon_url ='https://www.amazon.com/s?k={sear}&ref=nb_sb_noss_2'
walmart_url = 'https://www.walmart.com/search/?page=1&query={}'
bj_url = 'https://www.bjs.com/search/{}/q'
ebay_url= 'https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=0&_sop=12&_pgn=1'

# Create your views here.
def AppPage(request):

    search = request.POST.get('search')

    walmart_final_url = walmart_url.format(quote_plus(search))
    walmart_link = requests.get(walmart_final_url, auth=('user', 'pass'))
    walmart_data = walmart_link.text
    walmart_soup = BeautifulSoup(walmart_data, features='html.parser')

    walmart_output = str(walmart_soup.find_all('script', {'id':'searchContent'}))

    total_prod = walmart_output.count("productId")

    newlist = walmart_output.split("productId")

    walmart_list = []

    for i in range(1,total_prod):
        walmart_item_image = 'https://image.shutterstock.com/image-illustration/black-linear-photo-camera-logo-260nw-1412111903.jpg'
        if ('offerPrice') in str(newlist[i]):
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

            if 'imageUrl' in str(newlist[i]):
                walmart_item_image = newlist[i].split('imageUrl')[1].split(',')[0].replace("\"","").lstrip(':')
            elif 'srcSet' in str(newlist[i]):
                walmart_item_image = newlist[i].split('srcSet')[1].split(',')[0].replace("\"","").lstrip(':')
            elif 'productImageUrl' in str(newlist[i]):
                continue

            if 'customerRating' in newlist[i]:
                walmart_item_rating= newlist[i].split('customerRating')[1].split(',')[0].replace("\"","").replace(":","")

            else:
                walmart_item_rating = 0

        elif('minPrice') in str(newlist[i]):

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

            if 'imageUrl' in str(newlist[i]):
                walmart_item_image = newlist[i].split('imageUrl')[1].split(',')[0].replace("\"","").lstrip(':')
            elif 'srcSet' in str(newlist[i]):
                walmart_item_image = newlist[i].split('srcSet')[1].split(',')[0].replace("\"","").lstrip(':')
            elif 'productImageUrl' in str(newlist[i]):
                continue

            if 'customerRating' in newlist[i]:
                walmart_item_rating= newlist[i].split('customerRating')[1].split(',')[0].replace("\"","").replace(":","")

            else:
                walmart_item_rating = 0

        else:
            continue

        walmart_shipping = 'Above $35 Free Shipping'
        price_sort = float(walmart_item_price)
        walmart_list.append((walmart_item_title,walmart_item_url,walmart_item_image,'$'+walmart_item_price,walmart_shipping,walmart_item_seller,walmart_item_rating,price_sort,'Walmart'))

    ebay_final_url = ebay_url.format(quote_plus(search))
    ebay_link = requests.get(ebay_final_url, auth=('user', 'pass'))

    ebay_data = ebay_link.text
    ebay_soup = BeautifulSoup(ebay_data, features='html.parser')
    ebay_listings = ebay_soup.find_all('li', {'class': 's-item'})
    ebay_list = []

    for item in range(1,len(ebay_listings)-2):
        ebay_title = ebay_listings[item].find(class_='s-item__title').text
        ebay_link = ebay_listings[item].find('a', {'class':'s-item__link'}).get('href')
        ebay_img_link = ebay_listings[item].find('img', {'class':'s-item__image-img'}).get('src')
        if 'SECONDARY_INFO' in str(ebay_listings[item]):
            ebay_second_info = ebay_listings[item].find('span', {'class':'SECONDARY_INFO'}).text
        else:
            ebay_second_info = 'No info'
        ebay_price = ebay_listings[item].find('span', {'class':'s-item__price'}).text
        ebay_price = ebay_listings[item].find('span', {'class':'s-item__price'}).text

        if 'stars' not in (str(ebay_listings[item].find('span', {'class':'clipped'}))):
            ebay_rating = 'No Rating'
        else:
            ebay_rating = str(ebay_listings[item].find('span', {'class':'clipped'}).text).split(' ')[0]


        ebay_price_str = str(ebay_price)
        if 'Tap' in ebay_price_str:
            continue

        ebay_shipping = str(ebay_listings[item].find('span', {'class':'s-item__shipping s-item__logisticsCost'}))
        if ('Free' in ebay_shipping) or (ebay_shipping =='None') :
            ebay_shipping = 0
        else:
            ebay_shipping = float(ebay_shipping.split('$')[1].split(' ')[0])

        price_sort = float(ebay_price.split(' ')[0].replace("$","").replace(",",'')) + ebay_shipping


        ebay_list.append((ebay_title,ebay_link,ebay_img_link,ebay_price,ebay_shipping,ebay_second_info,ebay_rating,price_sort,'Ebay'))

    bj_final_url = bj_url.format(quote_plus(search))
    bj_link = requests.get(bj_final_url)

    bj_data = bj_link.text
    bj_soup = BeautifulSoup(bj_data, features='html.parser')

    bj_listings = bj_soup.find_all('div', {'class': 'flex-item-container'})
    bj_list = []

    for item in range(0,len(bj_listings),2):
        if 'Member Only Price' not in  str(bj_listings[item]):
            bj_title = bj_listings[item].find(class_='product-title no-select d-none d-sm-block').text
            bj_link = ('https://www.bjs.com'+bj_listings[item].find('a', {'class':'product-link mt-xl-3 mt-xs-3 mt-md-0 mt-3'}).get('href'))
            bj_img_link = bj_listings[item].find('img', {'class':'img-link'}).get('src')
            bj_price = bj_listings[item].find('span', {'class':'price'}).text

            bj_seller = "BJ's Wholesale"

            if 'Free Shipping' in str( bj_listings[item]):
                bj_shipping = bj_listings[item].find('span', {'class':'free-shipping'}).text
            else:
                bj_shipping = 'Shipping Not Included'

            if "star" in str(bj_listings[item]):
                full = str(bj_listings[item]).count('star on')/2
                half = str(bj_listings[item]).count('star half')/4
                bj_rating =full+half
            else:
                bj_rating = 'No Ratings'

            price_sort = float(bj_price.split(' ')[0].replace("$","").replace(",",''))
        else:
            continue
        bj_list.append((bj_title,bj_link,bj_img_link,bj_price,bj_shipping,bj_seller,bj_rating,price_sort,"bjs.com"))

    combined_list = walmart_list + ebay_list +bj_list

    # take second element for sort
    def takeSecond(elem):
        return elem[7]
    # sort list with key
    combined_list.sort(key=takeSecond)

    return render(request,'my_app/app_name.html',context = {'combined_list':combined_list})
