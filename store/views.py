from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,DetailView
from django.contrib.auth import authenticate,login,logout
from store.forms import RegistrationForm,LoginForm
from django.contrib import messages
from store.models import Product,BasketItem,Size
# Create your views here.

# url:localhost:8000/registration
# method get,post
# form:registration form
class SignUpView(View):

    def get(self,request,*args,**kwargs):
        form=RegistrationForm
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render(request,"login.html",{"form":form})


# url:localhost:8000/sigin
# method get,post 
# form_class:LoginForm
class SignInView(View):

    def get(self,request,*args,**kwargs):
        form=LoginForm
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("index")
        messages.error(request,"invalid credentials")
        return render(request,"login.html",{"form":form})



class IndexView(TemplateView):

    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()
        return render(request,"index.html",{"data":qs})



# url:localhost:8000/product/{id}
class ProductDetailView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Product.objects.get(id=id)
        return render(request,"product_details.html",{"data":qs})
    
# url:localhost:8000/product/{id}
# class ProductDetailView(DetailView):
#     template_name="product_details.html"
#     model=Product
#     context_object_name="data"


class HomeView(TemplateView):
    template_name="base.html"



# add to basket
# url:localhost:8000/product/{id}/add_to_basket/
# method:post
    
class AddToBasketView(View):

    def post(self,request,*args,**kwargs):
        size=request.POST.get("size")
        size_obj=Size.objects.get(name=size)
        qty=request.POST.get("qty")
        id=kwargs.get("pk")
        product_obj=Product.objects.get(id=id)
        BasketItem.objects.create(
            size_object=size_obj,
            qty=qty,
            product_object=product_obj,
            basket_object=request.user.cart
        )
        return redirect("index")
    

# basket item list view
# url:localhost:8000/basket/item/all
# method:get
    
class BasketItemView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitem.filter(is_order_placed=False)
        # qs=BasketItem.objects.filter(is_order_placed=False,
        #                              basket_object=request.user.cart
        #                              )
        return render(request,"cart_list.html",{"data":qs})
    

# basket item remove
# localhost:8000/basket/items/<id>/remove/
    
class BasketItemRemoveView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        basket_item_object.delete()
        return redirect ("basket-list")
    

# Basket item quantity update
# method:post
class CartItemUpdateQuantityView(View):

    def post(self,request,*args,**kwargs):
        action=request.POST.get("counterButton")
        print(action)
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)

        if action=="+":
            basket_item_object.qty+=1
        else:
            basket_item_object.qty-=1
        basket_item_object.save()

        return redirect("basket-list")
    

class CheckOutView(View):

    def get(self,request,*args,**kwargs):
        return render (request,"checkout.html")
    
    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        print(email,phone,address)
        return redirect ("index")