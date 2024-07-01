from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django_select2 import forms as s2forms

from .models import ClassGroups, Item, ItemOrder, Order, Users


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=False, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "password-input"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    # Add an additional field for password strength
    password_strength = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = Users
        fields = ("username", "email", "role", "student_id", "name")


class StudentWidget(s2forms.Select2MultipleWidget):
    search_fields = [
        "name__icontains",
        "email__icontains",
    ]


class ItemWidget(s2forms.Select2Widget):
    search_fields = [
        "name__icontains",
    ]


class GroupForm(forms.ModelForm):
    class Meta:
        model = ClassGroups
        fields = ["year", "term", "number", "professor", "student"]
        widgets = {"student": StudentWidget}

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields["student"].queryset = Users.objects.filter(role="student")
        self.fields["professor"].queryset = Users.objects.filter(role="teacher")

class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = ClassGroups
        fields = ["year", "term", "number", "professor", "student"]
        widgets = {
            "student": StudentWidget,
            "number": forms.HiddenInput(),
            "year": forms.HiddenInput(),
            "term": forms.HiddenInput(),
            "professor": forms.HiddenInput(),
        }
        labels: {"student": "Agregar Estudiantes"}

    def __init__(self, *args, **kwargs):
        super(StudentGroupForm, self).__init__(*args, **kwargs)
        self.fields["student"].queryset = Users.objects.filter(role="student")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["student"]
        widgets = {"student": StudentWidget}

    def __init__(self, group_pk: int, user_pk: int, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields["student"].queryset = Users.objects.filter(
            role="student", groups__in=group_pk
        ).exclude(pk=user_pk)


class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemOrder
        fields = ["item", "quantity", "code"]
        widgets = {"item": ItemWidget}


class UpdateOrderItemForm(forms.ModelForm):
    RESTRICTED_CHOICES = {
        "Solicitado": (
            ("Solicitado", "Solicitado"),
            ("Prestado", "Prestado"),
            ("Denegado", "Denegado"),
        ),
        "Prestado": (
            ("Solicitado", "Solicitado"),
            ("Prestado", "Prestado"),
            ("Devuelto", "Devuelto"),
        ),
        "Devuelto": (
            ("Prestado", "Prestado"),
            ("Devuelto", "Devuelto"),
        ),
        "Denegado": (
            ("Solicitado", "Solicitado"),
            ("Denegado", "Denegado"),
        ),
    }

    class Meta:
        model = ItemOrder
        fields = ["item", "quantity", "code", "status"]
        widgets = {
            "item": forms.HiddenInput(),
            "quantity": forms.NumberInput(attrs={"style": "text-align: center"}),
            "code": forms.TextInput(attrs={"style": "text-align: center"}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateOrderItemForm, self).__init__(*args, **kwargs)
        self.fields["status"].choices = self.RESTRICTED_CHOICES[self.instance.status]
