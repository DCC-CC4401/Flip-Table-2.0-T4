from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from account.forms import ClientCreateForm, PeddlerCreateForm, EstablishedCreateForm
from account.forms import ClientUpdateForm, PeddlerUpdateForm, EstablishedUpdateForm
from account.models import Client, Peddler, Established


class AccountCreateView(TemplateView):
    template_name = 'account/register_base.html'


class ClientCreateView(CreateView):
    template_name = 'account/register_client.html'
    form_class = ClientCreateForm

    def form_valid(self, form):
        valid = super(ClientCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

    def get_success_url(self):
        return reverse('homepage:index')


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'account/edit-client.html'
    fields = ['first_name', 'last_name', 'email', 'f_peddler', 'f_established', 'image']

    def form_valid(self, form):
        self.object = form.save()
        self.object.image = form.cleaned_data['image']
        print(form.cleaned_data)
        print(super(ClientUpdateView, self).get_form_class())
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('homepage:index')


class PeddlerCreateView(CreateView):
    template_name = 'account/register_peddler.html'
    form_class = PeddlerCreateForm

    def form_valid(self, form):
        valid = super(PeddlerCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

    def get_success_url(self):
        return reverse('homepage:index')


class PeddlerUpdateView(UpdateView):
    model = Peddler
    template_name = 'account/edit-peddler.html'
    form_class = PeddlerUpdateForm

    def get_success_url(self):
        return reverse('showcase:seller_detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

    # def get_form_class(self):
    #     form = super(PeddlerUpdateView, self).get_form_class()
    #     # form.fields.pop('username')
    #     # form.fields.pop('password1')
    #     # form.fields.pop('password2')
    #     return form


class EstablishedCreateView(CreateView):
    template_name = 'account/register_established.html'
    form_class = EstablishedCreateForm

    def form_valid(self, form):
        valid = super(EstablishedCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

    def get_success_url(self):
        return reverse('homepage:index')


class EstablishedUpdateView(UpdateView):
    model = Established
    template_name = 'account/edit-established.html'
    fields = ['first_name', 'last_name', 'email', 'image', 'cash', 'credit', 'debit', 'social', 'start', 'end']

    def get_success_url(self):
        return reverse('homepage:index')


@login_required(login_url='/account/login')
def edit_user(request, pk):
    if Peddler.objects.filter(id=pk).exists():
        return redirect('account:edit-peddler', pk)
    elif Client.objects.filter(id=pk).exists():
        return redirect('account:edit-client', pk)
    elif Established.objects.filter(id=pk).exists():
        return redirect('account:edit-established', pk)
    else:
        return redirect('homepage:index')


def success(request, algo):
    messages.add_message(request, messages.SUCCESS, "¡Has sido registrado con éxito!")
    return redirect('homepage:index')


@login_required(login_url='/account/login')
def delete_user(request):
    return render(request, 'account/delete.html')


@login_required(login_url='/account/login')
def confirm_deleted(request):
    request.user.delete()
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Usuario eliminado exitosamente")
    return render(request, 'account/deleted_confirmation.html')

def profile(request):
    return redirect('homepage:index')