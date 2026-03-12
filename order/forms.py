from django import forms

class CheckoutForm(forms.Form):
    shipping_name = forms.CharField(max_length=100, label='Ім\'я отримувача')
    shipping_city = forms.CharField(max_length=100, label='Місто')
    shipping_street = forms.CharField(max_length=255, label='Вулиця')
    shipping_zip_code = forms.CharField(max_length=20, label='Поштовий індекс')

    comment = forms.CharField(widget=forms.Textarea, required=False, label='Коментар до замовлення')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})