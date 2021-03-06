import datetime
import simplejson
from django.shortcuts import get_object_or_404
from django.shortcuts import render, reverse
from django.utils import timezone
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.views import View
from django.views.generic import DetailView

from .models import Transaction

from account.models import Client, Peddler, Established, Seller
from showcase.models import Dish

from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from showcase.forms import DishForm


class SellerDetailView(DetailView):
    template_name = 'showcase/showcase.html'
    context_object_name = 'seller'

    def get_context_data(self, **kwargs):
        context = super(SellerDetailView, self).get_context_data(**kwargs)
        context['is_peddler'] = hasattr(self.object, 'peddler')
        context['is_client'] = self.request.user.is_authenticated() and Client.objects.filter(
            pk=self.request.user.id).exists()
        context['is_favorite'] = self.object.client_set.filter(pk=self.request.user.id).exists()
        context['in_own_showcase'] = self.request.user.is_authenticated() and self.request.user.id == self.object.id
        context['dishes'] = self.object.dish_set.all()
        context['is_available'] = self.is_available()
        return context

    def get_object(self, queryset=None):
        seller_id = self.kwargs.get(self.pk_url_kwarg)
        if Peddler.objects.filter(pk=seller_id).exists():
            return Peddler.objects.get(pk=seller_id)
        else:
            return get_object_or_404(Established, pk=seller_id)

    def is_available(self):
        now = datetime.datetime.now().time()
        is_available = False
        try:
            start = self.object.start
            end = self.object.end
            if start <= end:
                if start <= now < end:
                    is_available = True
            else:
                if start <= now or now < end:
                    is_available = True
        except:
            is_available = False
        return is_available



# class Favorite(View):
#     def get(self, request, pk):
#         client = get_object_or_404(Client, pk=pk)
#         if Peddler.objects.filter(pk=pk).exists():
#             seller = Peddler.objects.get(pk=pk)
#             if client.f_peddler.filter(id=seller.id).exists():
#                 client.f_peddler.remove(seller)
#             else:
#                 client.f_peddler.add(seller)
#         else:
#             seller = Established.objects.get(pk=pk)
#             if client.f_established.filter(id=seller.id).exists():
#                 client.f_established.remove(seller)
#             else:
#                 client.f_established.add(seller)
#         client.save()
#         return HttpResponse(status=204)



class FavoriteView(View):
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=request.user.id)
        if Peddler.objects.filter(pk=pk).exists():
            seller = Peddler.objects.get(pk=pk)
            if client.f_peddler.filter(id=seller.id).exists():
                client.f_peddler.remove(seller)
            else:
                client.f_peddler.add(seller)
        else:
            seller = Established.objects.get(pk=pk)
            if client.f_established.filter(id=seller.id).exists():
                client.f_established.remove(seller)
            else:
                client.f_established.add(seller)
        client.save()
        return HttpResponse(status=204)


class StockView(View):
    def post(self, request, pk):
        new_stock = int(request.POST.get("stock_count", ""))
        dish_id = request.POST.get("dish_id", "")
        dish = get_object_or_404(Dish, id=dish_id)
        old_stock = dish.stock
        if new_stock < old_stock:
            dish.sold = old_stock - new_stock
            # seller = User.objects.get(id=pk)
            # transaction = Transaction(user=seller, dish=dish, price=dish.price, quantity=dish.sold)
            # transaction.save()
        dish.stock = new_stock
        dish.save()
        dish.save()
        return HttpResponse(status=204)


class DishCreateView(CreateView):
    template_name = 'showcase/dish.html'
    form_class = DishForm
    model = Dish
    context_object_name = 'dish'

    def form_valid(self, form):
        form.instance.seller = get_object_or_404(Seller, pk=self.kwargs.get(self.pk_url_kwarg))
        form.instance.icon = "img/" + dict(form.fields['choices'].choices)[form.cleaned_data['choices']]
        return super(DishCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('showcase:seller_detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

    def get_context_data(self, **kwargs):
        context = super(DishCreateView, self).get_context_data(**kwargs)
        context['can_delete'] = False
        return context


class DishUpdateView(UpdateView):
    template_name = 'showcase/dish.html'
    form_class = DishForm
    model = Dish
    context_object_name = 'dish'

    def get_object(self, queryset=None):
        return Dish.objects.get(pk=self.kwargs['dish_id'])

    def form_valid(self, form):
        form.instance.seller = get_object_or_404(Seller, pk=self.kwargs.get(self.pk_url_kwarg))
        form.instance.icon = "img/" + dict(form.fields['choices'].choices)[form.cleaned_data['choices']]
        return super(DishUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('showcase:seller_detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

    def get_context_data(self, **kwargs):
        context = super(DishUpdateView, self).get_context_data(**kwargs)
        context['can_delete'] = True
        return context


class DishDeleteView(DeleteView):
    model = Dish

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_object(self, queryset=None):
        return Dish.objects.get(pk=self.kwargs['dish_id'])

    def get_success_url(self):
        return reverse('showcase:seller_detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})


#def statistics(request):
#    return render(request, 'showcase/statistics.html')


def statistics(request):
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
              'Noviembre', 'Diciembre']
    earnings = {}
    for i, month in enumerate(months):
        sum = 0
        for item in Transaction.objects.all():
            if item.date.month == i + 1 and request.user.username == item.user.username:
                sum += item.price * item.quantity
        earnings[month] = sum
    return render(request, 'showcase/statistics.html', {'months': months, 'earnings': earnings})


class CheckIn(View):
    def get(self, request, seller_id):
        seller_profile = get_object_or_404(Peddler, id=seller_id)
        if seller_profile.available:
            seller_profile.available = False
        else:
            seller_profile.available = True
        seller_profile.save()
        return HttpResponse(status=204)
