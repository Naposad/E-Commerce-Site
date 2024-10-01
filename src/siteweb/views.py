from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView, DeleteView, UpdateView, ListView, FormView

from .forms import ContactForm

from .models import Products, Category, Order, OrderProducts
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Order , Contact # Exemple de mo
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

class CreateCategoryView(CreateView):
    model = Category
    template_name = 'siteweb/createCategory.html'
    success_url = reverse_lazy('')
    fields = '__all__'


class ListCategoryView(ListView):
    template_name = 'siteweb/listCategory.html'
    model = Category
    context_object_name = 'category'


class UpdateCategoryView(UpdateView):
    model = Category
    template_name = 'siteweb/updateCategory.html'


class DeleteCategory(DeleteView):
    model = Category
    success_url = reverse_lazy('')


class CreateProductsView(CreateView):
    model = Products
    template_name = 'siteweb/createProduct.html'
    fields = ['category', 'name', 'image', 'description', 'price', 'stock', 'status']

    def get_success_url(self):
        return reverse_lazy('detail-product', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.image = self.request.FILES.get('image', form.instance.image)  # Traiter l'image
        return super().form_valid(form)
    

class DetailProductsView(DeleteView):
    model = Products
    template_name = 'siteweb/detailProduct.html'
    context_object_name = 'product'


class ListProductsView(ListView):
    template_name = 'siteweb/listProducts.html'
    model = Products
    context_object_name = 'products'
    
    def get_queryset(self):
        return Products.objects.filter(status=True)


class UpdateProductsView(UpdateView):
    model = Products
    template_name = 'siteweb/updateProducts.html'
    fields = ['category', 'name', 'image', 'description', 'price', 'stock', 'status']

    def get_success_url(self):
        return reverse_lazy('detail-product', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image', form.instance.image)  # Traiter l'image
        return super().form_valid(form)


class DeleteProducts(DeleteView):
    template_name = 'siteweb/confDelete.html'
    model = Products
    context_object_name = 'product'
    success_url = reverse_lazy('list-product')

    """""def" get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_product = OrderProducts.get_total_quantity()
        context['order_product'] = order_product
"""""

class AddOrder(View):
    def post(self, request, product_id):
        products = get_object_or_404(Products, id=product_id)

        order, created = Order.objects.get_or_create(user=request.user, is_actif=True)

        order_products, created = OrderProducts.objects.get_or_create(order=order, products=products)
        if not created:
            order_products.quantity += 1
            order_products.save()
            return redirect('detail-product', slug=products.slug)


class OrderProduct(ListView):
    model = OrderProducts
    template_name = 'siteweb/orderProducts.html'
    context_object_name = 'order_product'

    def get_queryset(self):
        queryset = OrderProducts.objects.filter(order=self.request.user.order)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = sum(item.get_totale_price() for item in self.get_queryset())
        return context



class ListProducts(ListView):
    template_name = 'siteweb/listProducts-products.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 3
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
                return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(status=True)
    
    

@login_required
def profile_view(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {
        'user': user,
        'orders': orders,
    }
    return render(request, 'siteweb/profile.html', context)


class ListProductsElectronic(ListView):
    template_name = 'siteweb/electronicProduct.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 3
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
                return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Electronique').id,status=True)
    
    
    

class ListProductsSport(ListView):
    template_name = 'siteweb/sportProduct.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 3
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
                return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Sports & Loisirs').id,status=True)
    

class ListProductsMachine(ListView):
    template_name = 'siteweb/machineProduct.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 3
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
                return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Machines').id,status=True)
    
class ListProductsEmballage(ListView):
    template_name = 'siteweb/emballageProduct.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 3
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
                return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Emballage et impression').id,status=True)
    
    
class ListProductsVetement(ListView):
    template_name = 'siteweb/vetementProduct.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 3
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
                return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Vêtements').id,status=True)
    
    
    
class ContactView(CreateView):
    form_class = ContactForm
    model = Contact
    template_name = 'siteweb/contact.html'
    success_url = reverse_lazy('contact')  # Rediriger après soumission

    def form_valid(self, form):
        # Enregistrer les données du formulaire
        response = super().form_valid(form)
        # Afficher un message de succès
        messages.success(self.request, 'Merci pour votre message, nous vous contacterons bientôt.')
        return response

    def form_invalid(self, form):
        # Afficher un message d'erreur si le formulaire est invalide
        messages.error(self.request, 'Veuillez corriger les erreurs ci-dessous.')
        return super().form_invalid(form)