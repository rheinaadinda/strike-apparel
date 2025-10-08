from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# Create your views here.
def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    category = request.GET.get("category", "")  # ambil kategori dari query string
    
    # filter all / my product
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user).order_by('id')
    
    # filter berdasarkan kategori
    if category:
        product_list = product_list.filter(category__iexact=category)  
    
    context = {
        'app' : 'Strike Apparel',
        'name': 'Rheina Adinda Morani Sinurat',
        'npm' : '2406435881',
        'class': 'PBP E',
        'product_list': product_list,
        'last_login' : request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)
    
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'is_featured': product.is_featured,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, product_id):
    try:
        product_list = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_list)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product_list = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product_list])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.method == "POST":
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': 'Your account has been successfully created!',
                    'redirect_url': reverse('main:login')
                })
            else:
                messages.success(request, 'Your account has been successfully created!')
                return redirect('main:login')
        else:
            if is_ajax:
                # Kembalikan semua error form dalam format JSON
                errors = {}
                for field, errs in form.errors.items():
                    errors[field] = [{'message': e} for e in errs]
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = JsonResponse({
                'success': True,
                'redirect_url': reverse("main:show_main")
            }) if is_ajax else None

            if is_ajax:
                # set cookie lewat response JSON
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            else:
                resp = HttpResponseRedirect(reverse("main:show_main"))
                resp.set_cookie('last_login', str(datetime.datetime.now()))
                return resp
        else:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'errors': {'__all__': [{'message': 'Username atau password salah.'}]}
                }, status=400)
            else:
                from django.contrib.auth.forms import AuthenticationForm
                form = AuthenticationForm(request)
                return render(request, 'login.html', {'form': form, 'error': 'Username atau password salah.'})
    
    # GET request
    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    user = request.user

    new_product = Product(
        name=name, 
        price=price,
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()

    rendered_card = render_to_string('card_product.html', {'product': new_product}, request=request)
    return JsonResponse({'html': rendered_card}, status=201)

def product_list_ajax(request):
    filter_opt = request.GET.get('filter', 'all')
    category = request.GET.get('category', '')
    products = Product.objects.all()

    if filter_opt == 'my' and request.user.is_authenticated:
        products = products.filter(user=request.user)
    if category:
        products = products.filter(category=category)

    html = render_to_string('product_grid.html', {'product_list': products, 'user': request.user})
    return HttpResponse(html)

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.filter(pk=product_id).values(
            'name', 'price', 'description', 'category', 'thumbnail', 'is_featured'
        ).first()
        
        if product:
            return JsonResponse(product, status=200)
        else:
            return JsonResponse({"error": "Product not found"}, status=404)
            
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    
@login_required
def show_json_by_id_ajax(request, id): # Ganti parameter product_id menjadi id agar sesuai dengan urls.py
    try:
        # Menggunakan .values() untuk mendapatkan QuerySet dari dictionaries
        product = Product.objects.filter(pk=id).values(
            'name', 'price', 'description', 'category', 'thumbnail', 'is_featured'
        ).first()
        
        if product:
             # Mengembalikan dictionary langsung sebagai JsonResponse
            # Pastikan kunci 'name' di form Anda sesuai dengan 'title' di Model
            product['title'] = product.pop('name') # Asumsi form Anda menggunakan 'name' tapi Model Anda menggunakan 'title'
            return JsonResponse(product, status=200)
        else:
            return JsonResponse({"error": "Product not found"}, status=404)
            
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    
@csrf_exempt
@require_POST
@login_required
def edit_product_entry_ajax(request, id):
    product_instance = get_object_or_404(Product, pk=id, user=request.user)

    form = ProductForm(request.POST, instance=product_instance)

    if form.is_valid():
        product_instance = form.save()  
        rendered_card = render_to_string('card_product.html', {'product': product_instance, 'user': request.user}, request=request)
        return JsonResponse({'html': rendered_card, 'message': 'Product updated successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid data', 'details': form.errors}, status=400)

@require_POST
def delete_product_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return JsonResponse({"success": True})