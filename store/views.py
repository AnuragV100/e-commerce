from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,DetailView
from django.contrib.auth import authenticate,login,logout
from store.forms import RegistrationForm,LoginForm
from django.contrib import messages
from store.models import Product
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
    