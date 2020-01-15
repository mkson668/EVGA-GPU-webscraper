import bs4
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup

# changes on wed 
evga_url = 'https://www.evga.com/products/productlist.aspx?type=0'
# get request for the webpage and store raw html
url_client = urlReq(evga_url)
raw_html = url_client.read()

url_client.close()
# use soup to performing parsing
page_soup = soup(raw_html, "html.parser")
all_product_containers = page_soup.find_all("div", attrs = {"class" : "list-item"})

filename = "listings.csv"
f = open(filename, "w")

headers = "name, original price, discount, final price, base clock, boost clock, VRAM, bandwidth, link\n"
f.write(headers)

for product in all_product_containers:
    # print(product.prettify())
    details = []

    img = product.div.a.img["src"]
    link = product.find("div", {"class":"pl-list-image"}).contents[1]["href"]

    name = product.find("div", {"class":"pl-list-image"}).contents[1]["title"]
    details_ul = product.find("div", {"class":"pl-list-info"}).ul.contents

    for li in details_ul:
        if li != '\n':
            details.append(li.text)
    
    discount = 0
    price_original = ""

    price_final_p = product.find("p", {"class":"pl-list-price"})
    price_final = price_final_p.text

    if price_final[0:1] != "$":
        if price_final == "TBD":
            price_final = "0.00"
        else:
            index_sym = price_final.index("$")
            price_final = price_final[index_sym:]

    if product.find("span", {"class":"price-was"}):
        price_original_span = product.find("span", {"class":"price-was"})
        price_original = price_original_span.text
        index_sym = price_original.index("$")
        price_original = price_original[index_sym:]
    else:
        price_original = price_final
        
    discount = float(price_original[1:]) - float(price_final[1:])
    discount = "$" + str(discount)

    # we will skip over length smaller than 5 since they are not performance oriented gpu's
    if (len(details) < 5):
        print("skipping " + name)
        continue


    print("Product Link: " + link)
    print("Product Name: " + name)
    print("Discount: " + str(discount))
    print("Original: " + price_original)
    print("Base Clock Speed: " + details[3])
    print("Boost Clock Speed: " + details[0])
    print("VRAM: " + details[2])
    print("Bandwidth: " + details[4])
    print("Price: " + price_final)
    
    f.write(name.replace(",", " |") + "," + 
            price_original + "," +
            discount + "," + 
            price_final + "," +
            details[3] + "," + 
            details[0] + "," + 
            details[2] + "," + 
            details[4] + "," + 
            "https://www.evga.com" + link + "\n")
 
f.close()