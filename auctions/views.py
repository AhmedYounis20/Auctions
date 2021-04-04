from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import listing,comment,bid,watchlist,User
from .forms import creatinglistform


from .models import User


def index(request):
    activated=listing.objects.filter(active=1)

    
    return render(request, "auctions/index.html",{'lists':activated})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
def watchlistview(request):
    watch=watchlist.objects.filter(user=request.user)


    return render(request,'auctions/watchlist.html',{'watchlist':watch})
def createlistingview(request):
    if request.method=='GET':
        creatingform=creatinglistform()

        return render(request,'auctions/create Listing.html',{'form':creatingform})
    else:
        resform=creatinglistform(request.POST)
        f=request.POST
        if resform.is_valid():
            a=listing()
            a.productname=f['productname']
            a.productdescription=f['productdescription']
            a.productcategory=f['productcategory']
            a.product_price=f['product_price']
            a.product_image_url=f['product_image_url']
            a.creator=request.user.username
            a.save()
            b=bid()
            b.product=a
            b.user=request.user
            b.bids=0
            b.save()

            return HttpResponse('done')
        else:
            return render(request,'auctions/create Listing.html',{'form':creatingform})
def categoriesview(request):
    randomlylists=listing.objects.all()
    categorieslist=[]
    for i in randomlylists:
        if i.productcategory not in categorieslist:
            categorieslist.append(i.productcategory)
    categorieslist.sort()

    return render(request,'auctions/categories.html',{'cat':categorieslist,'lists':randomlylists})
#//////////////////////////////////(category)###################3
def categoryview(request,cat):
    catylists=listing.objects.filter(productcategory=cat)
    return render(request,'auctions/category.html',{'cat':catylists})
#################################((( product page )))/////////////////////
def listview(request,num):
    details=listing.objects.get(pk=num)
    try:
        numberofbids=bid.objects.get(product=details)
    except :
        numberofbids=bid()
        numberofbids.bids=0
        numberofbids.user=User.objects.get(username=details.creator)
        numberofbids.product=details
        numberofbids.save()
        numberofbids=bid.objects.get(product=details)

    comments=comment.objects.filter(product=details)
    print(request.user.username)
    commenterror=False
    if request.method=='POST':
        f=request.POST
        if 'watch' in  f:
            try:
                a=watchlist.objects.get(user=request.user,product=details)
                a.delete()
                render(request,'auctions/productpage.html',{'product':details,'comments':comments,'commenterror':commenterror,'bids':numberofbids,'watch_delete':True})
            except:
                a=watchlist()
                a.user=request.user
                a.product=details
                a.save()
                render(request,'auctions/productpage.html',{'product':details,'comments':comments,'commenterror':commenterror,'bids':numberofbids,'bid_error':False})
        if 'comment' in f:
            if f['comment'].split()==[]:
                commenterror=True
            else:
                newcomment=comment()
                newcomment.comment=f['comment']
                newcomment.username=request.user
                newcomment.product=details
                newcomment.save()
        if 'close' in f:
            details.active=False
            details.winner=numberofbids.user.username
            details.save()
        if 'bid' in  f:
            if float(f['bid']) <= details.product_price:
                return render(request,'auctions/productpage.html',{'product':details,'comments':comments,'commenterror':commenterror,'bids':numberofbids,'bid_error':True})
            else:
                try:
                    numberofbids.user=request.user
                    numberofbids.bids=numberofbids.bids+1
                    numberofbids.save()
                except:
                    b=bid(detials,request.user,1)
                    b.save()
            details.product_price=f['bid']
            details.save()

    return render(request,'auctions/productpage.html',{'product':details,'comments':comments,'commenterror':commenterror,'bids':numberofbids})
#///////////////////////