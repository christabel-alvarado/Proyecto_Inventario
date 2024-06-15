from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

# Create your views here.
from django.views.generic.list import ListView
from .models import Item, Class, Users, ClassGroups


class ItemList(ListView):

    # specify the model for list view
    model = Item
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ItemList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("name")
        return qs


class ItemCreate(CreateView):
    # specify the model for create view
    model = Item

    # specify the fields to be displayed
    fields = ["name"]


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy("articulos")
    template_name = "page/confirm_delete.html"


class ClassList(ListView):

    # specify the model for list view
    model = Class
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ClassList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("name")
        return qs


class ClassCreate(CreateView):
    # specify the model for create view
    model = Class

    # specify the fields to be displayed
    fields = ["name", "code"]


class ClassGroupsList(ListView):

    # specify the model for list view
    model = ClassGroups
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        class_id = Class.objects.filter(code=self.kwargs.get('code'))
        qs = super(ClassGroupsList, self).get_queryset(*args, **kwargs)
        qs = qs.filter(class_id=class_id[0])
        return qs

    def get_context_data(self, **kwargs):
        class_id = Class.objects.filter(code=self.kwargs.get('code'))
        context = super().get_context_data(**kwargs)
        context["class"] = class_id[0]
        return context


class ClassGroupsCreate(CreateView):
    # specify the model for create view
    model = ClassGroups

    # specify the fields to be displayed
    fields = ["semester", "number", "professor", "class_id"]

    def get_initial(self):
        initial = super().get_initial()
        class_id = Class.objects.filter(code=self.kwargs.get('code'))
        print(class_id)
        initial['class_id'] = class_id
        return initial


class StudentList(ListView):

    # specify the model for list view
    model = Users
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        qs = qs.filter(role='student')
        qs = qs.order_by("name")
        return qs