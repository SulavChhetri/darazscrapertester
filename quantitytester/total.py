import requests
import json,csv,pandas as pd
import sys
sys.path.append("..")

with open('../files/stopwords.txt', 'r')as file:
        lines = [line.rstrip('\n') for line in file]

def scrape(searchitem):
    darazurl = 'https://www.daraz.com.np/catalog/?_keyori=ss&from=input&page=1&q=' +searchitem
    try:
        nameprice = searchitem+ 'price.csv'
        r = requests.get(darazurl).text
        jsonresponse = json.loads(r.split("window.pageData=")[1].split('</script>')[0])
        mainlist = jsonresponse['mods']['listItems']
        with open(f'../files/{nameprice}','w') as file:
            writer = csv.writer(file)
            writer.writerow(['Product name','Price'])
            for item in mainlist:
                price = 'Rs.'+ str(int(float(item['utLogMap']['current_price'])))
                writer.writerow([item['name'],price])
    except:
        return "Bad Url"

def stopwordsremover(sentence):
    nostopword_sentence =list()
    for item in sentence.split():
        if not item.lower() in lines:
            nostopword_sentence.append(item)
    return ' '.join(nostopword_sentence)

def remove_punctuation(sentence):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    finalsentence=""
    for item in sentence:
        if item not in punc:
            finalsentence+=item
    return finalsentence

def ngramcreator(strings,n_grams):
    finallist = []
    nostopword = stopwordsremover(strings)
    splitlist = remove_punctuation(nostopword).split()
    n_grams_range = len(splitlist)-n_grams+1
    if (len(splitlist)<n_grams):
        return [remove_punctuation(strings)]
    else:
        for x in range(n_grams_range):
            finalstring = '' 
            for i in range(n_grams):  
                finalstring =finalstring+' '+splitlist[x+i]
            finallist.append(finalstring.lstrip())
        return finallist


def quantitygen(item):
    quantitylist = ['Packs','packs','Pack of','pcs','Pieces','Pack','RamenPack']
    n_gram = ngramcreator(item,2)
    for items in n_gram:
        if not (''.join(items.split()).isalpha()):
            for ite in items.split():
                if ite in quantitylist:
                    for itee in items.split():
                        if itee.isnumeric():
                            return int(itee)

def weightgen(item):
    items = item.split()
    a = ''.join(items).lower()
    weight = []
    for i in range(len(a)):
        if a[i].isnumeric():
            weight.append(a[i])
            if a[i+1]=='g':
                return int(''.join(weight))
            elif a[i+1]=='k' and a[i+2]=='g':
                return int(''.join(weight))*1000
        else:
            weight= []

def csvquantity(searchitem):
    nameprice = searchitem+ 'price.csv'
    namequantity = searchitem +'quantity.csv'
    products = pd.read_csv(f'../files/{nameprice}')
    product_name= list(products['Product name'])
    product_price = list(products['Price'])
    with open(f'../files/{namequantity}','w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name','Price','Quantity','Weight','Unit of Weight'])
        for value in range(len(product_name)):
            quantity = quantitygen(product_name[value])
            if quantity==None:
                quantity =1
            weight = weightgen(product_name[value])
            if weight == None:
                writer.writerow([product_name[value],product_price[value],quantity,weight,None])
                continue
            writer.writerow([product_name[value],product_price[value],quantity,weight,'gm'])


def main(searchitem):
    try:
        csvquantity(searchitem)
    except:
        scrape(searchitem)
        csvquantity(searchitem)

def filechecker(filename):
    path ='../files/'+filename
    try:
        with open(path,'r') as f:
            f.readline()
            line = f.readline()
            if line == '':
                return "Empty"
            else:
                return "Not Empty"
    except:
        return "File not found"

main('sweet')
main('noodles')
main('biscuits')