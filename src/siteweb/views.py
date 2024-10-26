import random
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView, DeleteView, UpdateView, ListView, FormView

from .forms import ContactForm

from .models import Products, Category, Order, OrderProducts, Command, CommandProducts
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Order, Contact  # Exemple de mo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction



# Create your views here.

class CreateCategoryView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'siteweb/createCategory.html'
    success_url = reverse_lazy('')
    fields = '__all__'
    permission_required = ['siteweb.add_category']


class ListCategoryView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'siteweb/listCategory.html'
    model = Category
    context_object_name = 'category'
    permission_required = ['siteweb.view_category']


class UpdateCategoryView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    template_name = 'siteweb/updateCategory.html'
    permission_required = ['siteweb.change_category']


class DeleteCategory(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('')
    permission_required = ['siteweb.delete_products']


class CreateProductsView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Products
    template_name = 'siteweb/createProduct.html'
    fields = ['category', 'name', 'image', 'description', 'price', 'stock', 'status']
    permission_required = ['siteweb.add_products']

    def get_success_url(self):
        return reverse_lazy('detail-product', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.image = self.request.FILES.get('image', form.instance.image)  # Traiter l'image
        return super().form_valid(form)


class DetailProductsView(DetailView):
    model = Products
    template_name = 'siteweb/detailProduct.html'
    context_object_name = 'product'


class ListProductsView(ListView):
    template_name = 'siteweb/listProducts.html'
    model = Products
    context_object_name = 'products'

    def get_queryset(self):
        return Products.objects.filter(status=True)


class UpdateProductsView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Products
    template_name = 'siteweb/updateProducts.html'
    fields = ['category', 'name', 'image', 'description', 'price', 'stock', 'status']
    permission_required = ['siteweb.change_products']

    def get_success_url(self):
        return reverse_lazy('detail-product', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image', form.instance.image)  # Traiter l'image
        return super().form_valid(form)
    
    
    def get_queryset(self):
        queryst = Products.objects.filter(author=self.request.user)
        return queryst


class DeleteProducts(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'siteweb/confDelete.html'
    model = Products
    context_object_name = 'product'
    success_url = reverse_lazy('list-product')
    permission_required = ['siteweb.delete_products']

    """""def" get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_product = OrderProducts.get_total_quantity()
        context['order_product'] = order_product
"""""


class AddOrder(LoginRequiredMixin, View):
    def post(self, request, product_id):
        products = get_object_or_404(Products, id=product_id)

        order, created = Order.objects.get_or_create(user=request.user, is_actif=True)

        order_products, created = OrderProducts.objects.get_or_create(order=order, products=products)
        if not created:
            order_products.quantity += 1
            order_products.save()
            return redirect('detail-product', slug=products.slug)
        return redirect('detail-product', slug=products.slug)


class OrderProduct(LoginRequiredMixin, ListView):
    model = OrderProducts
    template_name = 'siteweb/orderProducts.html'
    context_object_name = 'order_product'

    def get_queryset(self):
        if hasattr(self.request.user, 'order'):
            # L'utilisateur a une commande, donc tu peux procéder
            order = self.request.user.order
            queryset = OrderProducts.objects.filter(order=order)

        else:
        # Gérer le cas où l'utilisateur n'a pas de commande
            queryset = OrderProducts.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = sum(item.get_totale_price() for item in self.get_queryset())
        return context


class ListProducts(ListView):
    template_name = 'siteweb/listProducts-products.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 10

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
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Electronique').id, status=True)


class ListProductsSport(ListView):
    template_name = 'siteweb/sportProduct.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Sports & Loisirs').id, status=True)


class ListProductsMachine(ListView):
    template_name = 'siteweb/machineProduct.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Machines').id, status=True)


class ListProductsEmballage(ListView):
    template_name = 'siteweb/emballageProduct.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Emballage et impression').id, status=True)


class ListProductsVetement(ListView):
    template_name = 'siteweb/vetementProduct.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return Products.objects.filter(name__icontains=q, status=True)
        return Products.objects.filter(category=Category.objects.get(name='Vêtements').id, status=True)


class ContactView(CreateView):
    form_class = ContactForm
    model = Contact
    template_name = 'siteweb/contact.html'
    success_url = reverse_lazy('contact')  # Rediriger après soumission

    def form_valid(self, form):
        # Enregistrer les données du formulaire
        response = super().form_valid(form)
        # Afficher un message de succès
        messages.success(self.request, 'Merci pour votre message, nous vous contacterons bientôt par email.')
        return response

    def form_invalid(self, form):
        # Afficher un message d'erreur si le formulaire est invalide
        messages.error(self.request, 'Veuillez corriger les erreurs ci-dessous.')
        return super().form_invalid(form)


class TableauBord(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'siteweb/tableau-de-bord.html'
    model = Products
    context_object_name = 'products'
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name='Fournisseur')

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return Products.objects.filter(name__icontains=q, author=self.request.user)
        # Filtre les produits de l'utilisateur connecté
        return Products.objects.filter(author=self.request.user)



class CommandView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        userConnect = request.user
        try:
            myorder = Order.objects.get(user=self.request.user)

            with transaction.atomic():
                # Création de la commande
                commande = Command.objects.create(
                    order=myorder,
                    status='payée',
                )
                # Copier les produits dans CommandProducts
                for item in myorder.orderproducts_set.all():
                    CommandProducts.objects.create(
                        user = userConnect,
                        command=commande,
                        product=item.products,
                        quantity=item.quantity,
                        price_at_purchase=item.products.price
                )

                # Suppression des produits associés à l'ordre
                OrderProducts.objects.filter(order=myorder).delete()

                # Sauvegarde de la commande
                commande.save()

            return redirect('lasts-command')

        except Order.DoesNotExist:
            return HttpResponse("Aucune commande en cours", status=404)
        
    
    

    
class HistoricCommand(LoginRequiredMixin, ListView):
    model = Command
    template_name = 'siteweb/lastsCommand.html'
    context_object_name = 'commands'
    
    def get_queryset(self):
        return Command.objects.filter(order=Order.objects.get(user=self.request.user)).order_by('date_on').prefetch_related('commandproducts_set')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class updateOrderProduct(UpdateView, LoginRequiredMixin):
    model = OrderProducts
    fields = ['quantity']
    template_name = 'siteweb/updateOrderProduct.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_name'] = Products.objects.get(slug=self.kwargs['slug'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('order-list-product')
