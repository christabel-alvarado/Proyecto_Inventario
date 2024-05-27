from django.urls import path

# importing views from views.py
from .views import ItemList, ItemCreate, ClassList, ClassCreate

urlpatterns = [
	path('articulos', ItemList.as_view(template_name='page/articulos.html'), name='articulos'),
	path('crear-articulo', ItemCreate.as_view(template_name='page/crear-articulo.html', success_url='articulos'), name='crear-articulo'),
	path('cursos', ClassList.as_view(template_name='page/cursos.html'), name='cursos'),
	path('crear-curso', ClassCreate.as_view(template_name='page/crear-curso.html', success_url='cursos'), name='crear-curso'),
]
