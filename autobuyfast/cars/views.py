from django.shortcuts import redirect, render
from .models import AutoSearch
from .forms import AutoSearchForm
from django.views.generic import ListView
from .filters import CarFilter

# Create your views here.
class CarsListview(ListView):
    model = AutoSearch
    template_name = 'cars/list.html'
    page_kwarg = 'page'
    paginate_by = 15
    allow_empty = True
    context_object_name = "cars"
    
    def get_context_data(self, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)
        context["cars_total"] = AutoSearch.objects.count()
        context["filter"] = CarFilter(request.GET, queryset=AutoSearch.objects.all())
        return context
    
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_buyer:
    #         return redirect(reverse_lazy('home'))
    #     return super().dispatch(request, *args, **kwargs)
    
    # def get_context_data(self, **kwargs):
    #     request = self.request
    #     context = super().get_context_data(**kwargs)
    #     context["cars_total"] = AutoSearch.objects.count()
    #     car_list = AutoSearch.objects.all()
    #     context["filter"] = CarFilter(request.GET, queryset=self.get_queryset())
    #     return context

    # def get_queryset(self):
    #     request = self.request
    #     queryset = super().get_queryset
    #     return CarFilter(request.GET, queryset=queryset).qs


cars_list_view = CarsListview.as_view()

class CarsSearchListview(ListView):
    model = AutoSearch
    template_name = 'cars/search_list.html'
    page_kwarg = 'page'
    paginate_by = 15
    allow_empty = True

    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()
        return CarFilter(request.GET, queryset=queryset).qs.distinct()

    def get_context_data(self, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)
        context["filter"] = CarFilter(request.GET, queryset=self.get_queryset())
        return context
    
filter_car_search_view = CarsSearchListview.as_view()


def home(request):
    f = CarFilter(request.GET, queryset=AutoSearch.objects.all())

    data = {
        "form":f.form,
    }
    return render(request, 'pages/home.html', data)