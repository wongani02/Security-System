from django import forms

from .models import SecuredDoor

class UserCardCreationForm(forms.Form):
    rfid_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-input mt-1.5 w-full rounded-lg bg-slate-150 px-3 py-2 ring-primary/50 placeholder:text-slate-400 hover:bg-slate-200 focus:ring dark:bg-navy-900/90 dark:ring-accent/50 dark:placeholder:text-navy-300 dark:hover:bg-navy-900 dark:focus:bg-navy-900', 'placeholder': '**** **** **** ****', 'x-model.debounce':'cardNumber'}
        )
    )
    name_on_card = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-input mt-1.5 w-full rounded-lg bg-slate-150 px-3 py-2 ring-primary/50 placeholder:text-slate-400 hover:bg-slate-200 focus:ring dark:bg-navy-900/90 dark:ring-accent/50 dark:placeholder:text-navy-300 dark:hover:bg-navy-900 dark:focus:bg-navy-900', 'placeholder':'John Doe', 'x-model.debounce':'nameOnCard'}
        )
    )
    doors_to_access = forms.ModelMultipleChoiceField(
        queryset=SecuredDoor.objects.all(),
    )