from django.shortcuts import get_object_or_404, redirect, render
from django_tables2 import SingleTableView
from django.db.models import Sum

from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    )

from .tables import ParqueTable, ZonaTable, LugarTable

from .forms import ParqueModelForm, ZonaModelForm, LugarModelForm, ParqueModelFormCreate, LugarModelFormCreate
from .models import Parque, Zona, Lugar
from .tables import ParqueTable

def index_view(request, *args, **kwargs):
    return render(request, "home.html", {})

class ZonaErrorView(TemplateView):
    template_name = "erro_zona.html"

class LugarErrorView(TemplateView):
    template_name = "erro_lugar.html"

class ErrorView(TemplateView):
    template_name = "erro_erro.html"

class ErrorErrorView(TemplateView):
    template_name = "err.html"

#==================================================================================================
#Parque

class ParqueCreateView(CreateView):
    template_name = 'parque/parque_create.html'
    form_class = ParqueModelFormCreate
    queryset = Parque.objects.all()

    def form_valid(self, form):
        return super().form_valid(form)



# class ParqueListView(ListView):
#     template_name = 'parque/parque_list.html'
#     queryset = Parque.objects.all()

class ParqueListView(SingleTableView):
    model=Parque
    table_class=ParqueTable
    template_name = 'parque/parque_list.html'

    def parque_list(request):
        table = ParqueTable(Parque.objects.all())
        return render(request, "parque_list.html",{"table":table})




class ParqueDetailView(DetailView):
    template_name = 'parque/parque_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Parque, id=id_)



class ParqueUpdateView(UpdateView):
    template_name = 'parque/parque_edit.html'
    form_class = ParqueModelForm
    queryset = Parque.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Parque, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)



class ParqueDeleteView(DeleteView):
    template_name = 'parque/parque_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Parque, id=id_)

    def get_success_url(self):
        return '../../'



#==================================================================================================
#Zona

# class ZonaListView(ListView):
#     template_name = 'zona/zona_list.html'
#     model = Zona

#     def get_queryset(self):
#         parque=Parque.objects.get(id=self.kwargs["id"])
#         return Zona.objects.filter(parqueid=parque)

class ZonaListView(SingleTableView):
    model=Zona
    table_class=ZonaTable
    template_name = 'zona/zona_list.html'

    def get_queryset(self):
        parque=Parque.objects.get(id=self.kwargs["id"])
        return Zona.objects.filter(parqueid=parque)

    def zona_list(request):
        table = ZonaTable(Zona.objects.all())
        return render(request, "zona_list.html",{"table":table})



class ZonaDetailView(DetailView):
    template_name = 'zona/zona_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Zona, id=id_)



class ZonaCreateView(CreateView):
    template_name = 'zona/zona_create.html'
    form_class = ZonaModelForm
    model = Zona

    def form_valid(self, form):
        zona = form.save(commit=False)
        zona.parqueid = Parque.objects.get(id=self.kwargs["id"])

        capacidade_input = form.cleaned_data.get("lugares")
        capacidade_existente = Zona.objects.filter(parqueid=zona.parqueid).aggregate(Sum('lugares'))

        zonas_possiveis = Parque.objects.get(id=zona.parqueid.id)
        zonas_existentes = Zona.objects.filter(parqueid=zona.parqueid).count()

        if(zonas_possiveis.zonas <= zonas_existentes):
            return redirect('erro/')

        if(capacidade_existente['lugares__sum'] == None):
            temp = 0
        else:
            temp = capacidade_existente['lugares__sum']

        if(temp+capacidade_input > zona.parqueid.capacidade):
            return redirect('erro/erro/')


        return super(ZonaCreateView, self).form_valid(form)
            

    def get_success_url(self):
        return '../'



class ZonaUpdateView(UpdateView):
    template_name = 'zona/zona_edit.html'
    form_class = ZonaModelForm
    model = Zona

    def form_valid(self, form):
        zona = form.save(commit=False)
        zona.parqueid = Parque.objects.get(id=self.kwargs["id"])

        capacidade_input = form.cleaned_data.get("lugares")
        capacidade_existente = Zona.objects.filter(parqueid=zona.parqueid).aggregate(Sum('lugares'))
        capacidade_existente_zona = Zona.objects.filter(id=zona.id).aggregate(Sum('lugares'))

        print(capacidade_existente['lugares__sum'])
        print(capacidade_existente_zona['lugares__sum'])

        if(capacidade_existente['lugares__sum'] == None):
            temp = 0
        else:
            temp = capacidade_existente['lugares__sum']

        if(temp+capacidade_input-capacidade_existente_zona['lugares__sum'] > zona.parqueid.capacidade):
            return redirect('erro/')

        return super(ZonaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return '../'




class ZonaDeleteView(DeleteView):
    template_name = 'zona/zona_delete.html'
    model = Zona

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        super().delete(*args, **kwargs)

    def get_success_url(self):
        return '../../'



#==================================================================================================
#Lugar

# class LugarListView(ListView):
#     template_name = 'lugar/lugar_list.html'
#     model = Lugar

#     def get_queryset(self):
#         zona=Zona.objects.get(id=self.kwargs["pk"])
#         return Lugar.objects.filter(zonaid=zona)

class LugarListView(SingleTableView):
    model=Lugar
    table_class=LugarTable
    template_name = 'lugar/lugar_list.html'

    def get_queryset(self):
        zona=Zona.objects.get(id=self.kwargs["pk"])
        return Lugar.objects.filter(zonaid=zona)

    def zona_list(request):
        table = LugarTable(Lugar.objects.all())
        return render(request, "lugar_list.html",{"table":table})



class LugarDetailView(DetailView):
    template_name = 'lugar/lugar_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("lugar")
        return get_object_or_404(Lugar, id=id_)



class LugarCreateView(CreateView):
    template_name = 'lugar/lugar_create.html'
    form_class = LugarModelFormCreate
    model = Lugar

    def form_valid(self, form):
        lugar = form.save(commit=False)
        lugar.zonaid = Zona.objects.get(id=self.kwargs["pk"])
        lugares_possiveis = Zona.objects.get(id=lugar.zonaid.id)
        lugares_existentes = Lugar.objects.filter(zonaid=lugar.zonaid).count()
        if(lugares_possiveis.lugares > lugares_existentes):
            return super(LugarCreateView, self).form_valid(form)
        else:
            return redirect('erro/')

    def get_success_url(self):
        return '../'



class LugarUpdateView(UpdateView):
    template_name = 'lugar/lugar_edit.html'
    form_class = LugarModelForm
    model = Lugar

    def get_object(self):
        id_ = self.kwargs.get("lugar")
        return get_object_or_404(Lugar, id=id_)

    def form_valid(self, form):
        lugar = form.save(commit=False)
        lugar.zonaid = Zona.objects.get(id=self.kwargs["pk"])
        return super(LugarUpdateView, self).form_valid(form)

    def get_success_url(self):
        return '../../'



class LugarDeleteView(DeleteView):
    template_name = 'lugar/lugar_delete.html'
    model = Lugar

    def get_object(self):
        id_ = self.kwargs.get("lugar")
        return get_object_or_404(Lugar, id=id_)

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        super().delete(*args, **kwargs)

    def get_success_url(self):
        return '../../'