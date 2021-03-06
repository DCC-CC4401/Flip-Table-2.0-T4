from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from account.models import Client, Peddler, Established


class ClientCreateForm(UserCreationForm):
    # CHOICES = (
    #     ('1', 'AvatarEstudiante1.png',),
    #     ('2', 'AvatarEstudiante2.png',),
    #     ('3', 'AvatarEstudiante3.png',),
    #     ('4', 'AvatarEstudiante4.png',))
    # choices = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super(ClientCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})
        # self.fields['choices'].widget.attrs.update({'class': 'with-gap'})

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'image')


class ClientUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(ClientUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'username', 'email', 'image')


class PeddlerCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(PeddlerCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['cash'].widget.attrs.update({'class': 'filled-in'})
        self.fields['credit'].widget.attrs.update({'class': 'filled-in'})
        self.fields['debit'].widget.attrs.update({'class': 'filled-in'})
        self.fields['social'].widget.attrs.update({'class': 'filled-in'})

    class Meta:
        model = Peddler
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'image', 'cash', 'credit',
                  'debit', 'social', 'available')


class PeddlerUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PeddlerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['cash'].widget.attrs.update({'class': 'filled-in'})
        self.fields['credit'].widget.attrs.update({'class': 'filled-in'})
        self.fields['debit'].widget.attrs.update({'class': 'filled-in'})
        self.fields['social'].widget.attrs.update({'class': 'filled-in'})

    class Meta:
        model = Peddler
        fields = ('first_name', 'last_name', 'email', 'image', 'cash', 'credit',
                  'debit', 'social')


class EstablishedCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(EstablishedCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['cash'].widget.attrs.update({'class': 'filled-in'})
        self.fields['credit'].widget.attrs.update({'class': 'filled-in'})
        self.fields['debit'].widget.attrs.update({'class': 'filled-in'})
        self.fields['social'].widget.attrs.update({'class': 'filled-in'})

    class Meta:
        model = Established
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'image', 'cash', 'credit',
                  'debit', 'social', 'start', 'end')


class EstablishedUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(EstablishedUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['cash'].widget.attrs.update({'class': 'filled-in'})
        self.fields['credit'].widget.attrs.update({'class': 'filled-in'})
        self.fields['debit'].widget.attrs.update({'class': 'filled-in'})
        self.fields['social'].widget.attrs.update({'class': 'filled-in'})

    class Meta:
        model = Established
        fields = ('first_name', 'last_name', 'username', 'email', 'image', 'cash', 'credit',
                  'debit', 'social', 'start', 'end')
