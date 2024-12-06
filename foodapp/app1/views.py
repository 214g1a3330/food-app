from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from app1.models import *

# Create your views here.

def render_home(request):
    '''messages.success(request, "I know You are Hungry.. I don't let my friends with hungry stomach")'''
    search_query = request.POST.get("ser")  # Retrieve search query from POST request
    if search_query:
        all_items = Fooditem.objects.filter(itemname__icontains=search_query)
    else:
        all_items = Fooditem.objects.all()
    
    if request.method == "POST" and not search_query:
        items = request.POST.get("items")
        all_items = Fooditem.objects.filter(itemtype=items)
    
    return render(request, "home.html", {"all": all_items})




@login_required(login_url="userlogin")
def add_cart(request, rid):
    obj = Fooditem.objects.get(id=rid)
    cart_item = Cart(item=obj)
    cart_item.save()
    messages.success(request, f"{cart_item.item.itemname} successfully added to the cart :)")
    return redirect("home")



def render_item_reg(request):
    if request.method == "POST":
        itempic = request.FILES.get("itempic")
        itemname = request.POST.get("itemname")
        price = request.POST.get("price")
        itemtype = request.POST.get("itemtype")
        rating = request.POST.get("rating")
        availability = request.POST.get("availability")
        obj = Fooditem(itempic=itempic, itemname=itemname, price=price, itemtype=itemtype, rating=rating, availability=availability)
        obj.save()
        messages.success(request, f"{itemname} successfully added to the menu :) please add more")
        return redirect("itemreg")
    return render(request, "item_register.html")



def render_user_login(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        pword = request.POST.get("pword")
        obj = authenticate(username=uname, password=pword)
        if obj:
            login(request, obj)
            messages.success(request, "You are successfully logged in")
            return redirect("home")
        messages.error(request, "Please enter valid credentials")
        return redirect("userlogin")
    return render(request, "user_login.html")



def render_user_reg(request):
    if request.method=="POST":
        uname=request.POST.get('uname')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('emailid')
        passw=request.POST.get('pword')
        cpass=request.POST.get('cpword')
        print(uname,fname,lname,email,passw,cpass)
        if User.objects.filter(username=uname).exists():
            messages.info(request,"Username already exists !")
            return redirect('userreg')
        if len(uname)<6:
            messages.info(request,"Bro Give lengthy username")
            return redirect('userreg')
        if passw.isalnum():
            messages.info(request,"Bro you should must give one special character")
            return redirect("userreg")
        
        if len(passw)<8:
            messages.info(request,"Password must contain 8 characters")
            return redirect('usereg')
        
        if (cpass!=passw):
            messages.info(request,"Bro both passwords should be same")
            return redirect('userreg')
        

        obj=User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=email,password=passw)
        obj.save()
        messages.success(request,"registration completed brooooo..Now Login now")
        return redirect('userlogin')
    return render(request, "user_register.html")



def render_single(request, rid):
    obj = Fooditem.objects.get(id=rid)
    return render(request, "single.html", {"obj": obj})



def logout_user(request):
    empty_cart(request)
    logout(request)
    return redirect("userlogin")



@login_required(login_url="userlogin")
def render_show_cart(request):
    all = Cart.objects.all()
    total = 0
    for i in all:
        total += i.item.price
    return render(request, "cart.html", {"all": all, "total": total})



def empty_cart(request):
    all = Cart.objects.all()
    all2 = Order.objects.all()
    for i in all:
        i.delete()
    for i in all2:
        i.delete()
    return redirect("showcart")


@login_required(login_url="userlogin")
def remove_item(request, rid):
    obj = Cart.objects.get(id=rid)
    if Order.objects.filter(items=obj).exists():
        obj2 = Order.objects.get(items=obj)
        obj2.delete()
    obj.delete()
    return redirect("showcart")



@login_required(login_url="userlogin")
def render_order(request):
    if request.method == "POST":
        addr = request.POST.get("addr")
        phno = request.POST.get("phno")
        order_items = Cart.objects.all()
        for i in order_items:
            obj = Order(usern=request.user, addr=addr, phno=phno, items=i)
            obj.save()
        messages.success(request, "Order placed successfully :D")
        return redirect("ordered")
    return render(request, "order.html")



@login_required(login_url="userlogin")
def render_ordered(request):
    total = 0
    all = Order.objects.all()
    obj = all[0]
    for i in all:
        total += i.items.item.price
    print(all)
    empty_cart(request)
    return render(request, "ordered.html", {"all": all, "total": total, "obj": obj})

