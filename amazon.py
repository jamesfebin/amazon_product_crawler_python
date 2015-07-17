import csv
import os
import urllib2
from bs4 import BeautifulSoup
import re


def init_file(filepath):
    try:
        with open(filepath, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
            writer.writerows([['ASIN URL','Title','Description','Brand','Price','List Price','Category','Shipping' , 'You Save', 'Features' , 'Image 1', 'Image 2', 'Image 3' , 'Image 4', 'Image 5']])
            #print 'file initialized'
    except Exception as e:
        print e


def append_to_file(filepath,row):
    try:
        with open(filepath, 'ab') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
            writer.writerows(row)
            #print 'writing'
    except Exception as e:
        print e


def readfile(filename):
      try:
           count =0
           output_file_path =  "output" + filename
           init_file(output_file_path)
           with open(filename) as csvfile:
              reader = csv.DictReader(csvfile)
              for row in reader:
                 try :
                   url = row['Affiliate Link']
                   page = urllib2.urlopen(url).read()
                   soup = BeautifulSoup(page,"lxml")

                   product_title = product_description = product_brand = product_price = product_list_price = product_category = product_shipping = product_you_save  = product_features = product_image_1 = product_image_2 = product_image_3 = product_image_4 = product_image_5 = ''

                   '''
                   Check if it's in stock, otherwise skip the product
                   '''

                   stock = soup.find('span',{'class':'a-size-medium a-color-success'})

                   if not stock: 
                      continue
                   soups = soup.findAll(attrs={"name":"description"})

                   #print 'Description'
                   if len(soups) > 0:
                     description = soups[0].get('content').encode('utf-8', 'ignore') 
                     product_description = description
                     #print description                 

                   title = soup.find('span',{'id':'productTitle'})
                   #print 'Title'

                   if title:
                      product_title = title.get_text().encode('utf-8', 'ignore') 
                      #print product_title
              
                   #print 'Brand'
                   brand = soup.find('a',{'id':'brand'})
                   if brand:
                       product_brand = brand.get_text().encode('utf-8', 'ignore') 
                       #print product_brand

                   #print 'Price'
                   price = soup.find('span',{'id':'priceblock_ourprice'})
                   if price:
                      product_price = price.get_text().encode('utf-8', 'ignore')  
                      #print product_price
                  
                   #print 'List Price'
                   list_price = soup.find('td',{'class':'a-span12 a-color-secondary a-size-base a-text-strike'})
                   if list_price:
                      product_list_price = list_price.get_text().encode('utf-8', 'ignore') 
                      #print product_list_price

                   #print 'Category'
                   category = soup.find('a',{'class':'nav-a nav-b nav-b'})
                   if category:
                      product_category = category.get_text().encode('utf-8', 'ignore') 
                      #print product_category

                   #print 'Shipping'
                   shipping = soup.find('span',{'class':'a-size-small a-color-secondary shipping3P'})
                   if shipping:
                      product_shipping =  shipping.get_text().encode('utf-8', 'ignore') 
                      #print product_shipping

                   #print 'You Save'
                   you_save = soup.find('tr',{'id':'regularprice_savings'})
                   if you_save:
                      product_you_save = you_save.get_text().encode('utf-8', 'ignore') 
                      #print product_you_save

                   #print 'Features'
                   feature = soup.find('div',{'id':'feature-bullets'})
                   if feature:
                      product_features = feature.get_text().encode('utf-8', 'ignore') 
                      #print product_features

                   #print 'Images'
                   images = soup.find('img',{'id':'landingImage'}) 
                   images = images.get('data-a-dynamic-image')
                   urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', images)
                   
                   if len(urls) == 0: 
                      continue

                   img_count = 0
                   for url in urls:
                      if img_count == 0: 
                        product_image_1 = url
                      elif img_count == 1:
                        product_image_2 = url
                      elif img_count == 2:
                        product_image_3 = url
                      elif img_count == 3:
                        product_image_4 = url
                      elif img_count == 4:
                        product_image_5 = url
                      img_count = img_count + 1
                   #print urls

                   append_to_file(output_file_path,[[url,product_title,product_description,product_brand,product_price,product_list_price,product_category,product_shipping,product_you_save,product_features,product_image_1,product_image_2,product_image_2,product_image_3,product_image_4,product_image_5]])

                   count = count + 1
                   print str(count) + "." + title.string

                 except Exception as e:
                   print e
      except Exception as e:
          print e


filename = raw_input("Enter input filename ")
if filename == '':
  #print 'Assuming file as input.csv '
  filename = 'input.csv'
readfile(filename)