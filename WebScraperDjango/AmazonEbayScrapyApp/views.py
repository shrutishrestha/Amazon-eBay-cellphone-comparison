from django.shortcuts import render

import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join("../WebScraperScrapy/WebScraperScrapy/ecommerce_items.db")


# Create your views here.
def home(request):
    conectionn = sqlite3.connect(db_path)
    cursorObj22 = conectionn.cursor()
    cursorObj22.execute('SELECT DISTINCT mobileid FROM "amazon_mobiles_reviews_tb" ')
    mobileReviews = cursorObj22.fetchall()

    mobileFullData = []
    cursorObj = conectionn.cursor()
    cursorObj.execute(
        'SELECT * FROM amazon_mobiles_tb WHERE operating_system!="N/A" AND screen_size!="N/A" AND memory_storage_capacity!="N/A" ')
    result = cursorObj.fetchall()

    # Append mobile data of those having reviews
    for res in result:
        for review in mobileReviews:
            if res[0] in review:
                mobileFullData.append(res)

    # Append mobile data not having reviews
    for res in result:
        flag = 0
        for review in mobileReviews:
            if review[0] in res:
                flag = 1
                break
        if (flag == 0):
            mobileFullData.append(res)

    return render(request, 'home.html', {'data': mobileFullData})


def phone_compare(request, phone_id):
    conectionn = sqlite3.connect(db_path)
    cursorObj = conectionn.cursor()
    cursorObj.execute('SELECT * FROM amazon_mobiles_tb WHERE mobileid = ? ', (phone_id,))

    result = cursorObj.fetchall()
    name = result[0][1]
    price = result[0][2]


    subStrName = str(' '.join(name.split()[:3]))
    subStrName2 = str(' '.join(name.split()[:2]))
    cursorObjNext = conectionn.cursor()
    cursorObjNext.execute(' SELECT * FROM ebay_mobiles_tb WHERE price > ? and price < ?', (price-500, price+500,))
    total_result = cursorObjNext.fetchall()
    similarItem = []
    for i in total_result:
        if (subStrName in i[1]):
            similarItem.append(i)
            if (len(similarItem) > 3):
                break
        break
    if not similarItem:
        for i in total_result:
            if (subStrName2 in i[1]):
                similarItem.append(i)
                if (len(similarItem) > 3):
                    break
    return render(request, 'comparison.html', {'data': result, 'name': name, 'similarItem': similarItem})


def phone_review(request, id):
    conectionn = sqlite3.connect(db_path)
    cursorObj = conectionn.cursor()
    cursorObj.execute('SELECT * FROM amazon_mobiles_reviews_tb WHERE mobileid = ?', (id,))
    result = cursorObj.fetchall()

    cursorObj12 = conectionn.cursor()
    cursorObj12.execute(
        'SELECT * FROM amazon_mobiles_tb WHERE mobileid = ? ',
        (id,))

    name = cursorObj12.fetchall()
    positive_review = []
    negative_review = []
    unlabelled_review = []

    for i in result:
        if i[2] != "N/A":
            positive_review.append(i[2])
        if i[3] != "N/A":
            negative_review.append(i[3])
        if i[4] != "N/A":
            unlabelled_review.append(i[4])

    if not positive_review:
        positive_review.append("N/A")
    if not negative_review:
        negative_review.append("N/A")
    if not unlabelled_review:
        unlabelled_review.append("N/A")

    return render(request, 'reviews.html',
                  {'data': result, 'name': name, 'positive_review': positive_review, 'negative_review': negative_review,
                   'unlabelled_review': unlabelled_review})
