from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import BadHeaderError, EmailMessage, send_mail, send_mass_mail
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView

from .filters import CarFilter, CarSearchFilter, HomeSearchFilter
from .forms import AutoSearchForm, CarImageFormset, ContactCarDealerForm
from .models import AutoSearch, CarCompare, WatchCars

User = get_user_model()

# Create your views here.

class CompareCreateView(SuccessMessageMixin, UpdateView):
    model = CarCompare
    template_name = "cars/compare.html"
    fields = ["car_one", "car_two", "car_three"]
    success_message = _("Successfully Compared our car ads")

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # try:
        #     obj = queryset.get()
        # except queryset.model.DoesNotExist:
        #     raise Http404(_("No %(verbose_name)s found matching the query") % {'verbose_name': queryset.model._meta.verbose_name}))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["results"] = CarCompare.objects.filter()
        return context

    def get_success_url(self):
        return reverse_lazy('cars:compare')#, kwargs={'slug':self.object.slug})

class CarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AutoSearch
    template_name = 'cars/create.html'
    form_class = AutoSearchForm
    success_message = _("Successfully created your car ad")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["images"] = CarImageFormset(self.request.POST, self.request.FILES)
        else:
            context["images"] = CarImageFormset()
        return context
    
    # def get_object(self):
    #     car = get_object_or_404(AutoSearch, slug=self.kwargs['slug'])
    #     return car

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        with transaction.atomic():
            form.instance.dealer = self.request.user
            form.instance.car_dealer_name = self.request.user.full_name
            form.instance.car_dealer_phone = self.request.user.phone_no
            self.object = form.instance.save()
            if images.is_valid():
                images.instance.car = self.object
                images.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        # car = get_object_or_404(AutoSearch, slug=self.kwargs['slug'])
        # return car.get_absolute_url()
        return reverse_lazy('cars:detail', kwargs={'slug':self.object.slug})

        


# user_update_view = UserUpdateView.as_view()


class CarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AutoSearch
    template_name = 'cars/update.html'
    slug_field = "slug"
    slug_url_kwarg = "slug"
    form_class = AutoSearchForm
    success_message = _("Successfully updated your car ad")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["images"] = CarImageFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context["images"] = CarImageFormset(instance=self.object)
        return context
    
    # def get_object(self):
    #     car = get_object_or_404(AutoSearch, slug=self.kwargs['slug'])
    #     return car

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        with transaction.atomic():
            form.instance.dealer = self.request.user
            form.instance.car_dealer_name = self.request.user.full_name
            form.instance.car_dealer_phone = self.request.user.phone_no
            self.object = form.instance.save()
            if images.is_valid():
                images.instance.car = self.object
                images.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        # car = get_object_or_404(AutoSearch, slug=self.kwargs['slug'])
        # return car.get_absolute_url()
        return reverse_lazy('cars:detail', kwargs={'slug':self.object.slug})




def CarDeleteView(request, slug):
    car = AutoSearch.objects.filter(available=True).get(slug=slug)
    car.delete()
    return HttpResponseRedirect(reverse('users:ads'))

def CarSold(request, slug):
    car = AutoSearch.objects.filter(available=True).get(slug=slug)
    car.available = False
    car.save()
    return HttpResponseRedirect(reverse('users:ads'))
class CarsListview(ListView):
    model = AutoSearch
    template_name = 'cars/list.html'
    ordering = ["-car_year", "-created"]
    page_kwarg = 'page'
    paginate_by = 20
    allow_empty = True
    context_object_name = "cars"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context["cars_total"] = AutoSearch.objects.count()
        context["filter"] = CarSearchFilter(request.GET, queryset=AutoSearch.objects.filter(available=True))
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
        return CarSearchFilter(request.GET, queryset=queryset).qs.distinct()

    def get_context_data(self, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)
        context["cars_total"] = self.get_queryset().count()
        context["filter"] = CarSearchFilter(request.GET, queryset=self.get_queryset())
        return context
    
filter_car_search_view = CarsSearchListview.as_view()


class CarsHomeSearchListview(ListView):
    model = AutoSearch
    template_name = 'cars/home_search_list.html'
    page_kwarg = 'page'
    paginate_by = 15
    allow_empty = True

    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()
        return HomeSearchFilter(request.GET, queryset=queryset).qs.distinct()

    def get_context_data(self, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)
        context["cars_total"] = self.get_queryset().count()
        context["filter"] = CarSearchFilter(request.GET, queryset=self.get_queryset())
        return context
    
filter_home_car_search_view = CarsHomeSearchListview.as_view()


def home(request):
    f = CarFilter(request.GET, queryset=AutoSearch.objects.filter(available=True))

    data = {
        "form":f.form,
    }
    return render(request, 'pages/home.html', data)

def base(request):
    f = CarSearchFilter(request.GET, queryset=AutoSearch.objects.filter(available=True))
    data = {
        "filter":f,
    }
    return render(request, 'cars/base.html', data)


# def CarLikeFunc(request, slug):
#     car = get_object_or_404(AutoSearch, slug=request.POST.get('carlike_id'))
#     if car.likes.filter(pk=request.user.id).exists():
#         car.likes.remove(request.user)
#         messages.error(request, "Disliked")
#     else:
#         car.likes.add(request.user)
#         messages.success(request, "Liked")
#     return HttpResponseRedirect(reverse_lazy('cars:detail', args=[str(slug)]))

@login_required
def watch_car(request, slug):
    car = get_object_or_404(AutoSearch, slug=slug)
    user = request.user

    if not WatchCars.objects.filter(user=user, car=car, active=True).exists():
        WatchCars.objects.create(user=user, car=car, active=True)
        messages.success(request, f"{car.title} added to your watch list")
    return HttpResponseRedirect(reverse('users:watch_list'))

@login_required
def unwatch_car(request, slug):
    car = get_object_or_404(AutoSearch, slug=slug)
    user = request.user
    unwatch = get_object_or_404(WatchCars, user=user, active=True, car=car)
    if WatchCars.objects.filter(user=user, car=car, active=True).exists():
        obj = unwatch
        obj.delete()
        messages.success(request, f"{car.title} removed from your watch list")
    return HttpResponseRedirect(reverse('users:watch_list'))


class CarDetailView(FormMixin, SuccessMessageMixin, DetailView):
    model = AutoSearch
    template_name='cars/detail.html'
    context_object_name = "car"
    form_class = ContactCarDealerForm
    success_message = "Your Message has been sent to the dealer"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        instance = self.get_object()
        email = form.cleaned_data['email']
        question = form.cleaned_data['question']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        message = form.cleaned_data['message']
        send_mail("Request Dealer", f"{first_name} {last_name} has made a dealer request\n {question},\n {message}\n Contact Information:\n {email}\n{phone}", email, [instance.dealer.email], fail_silently=False)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # likes_connected = get_object_or_404(AutoSearch, slug=self.kwargs['slug'])
        car_obj = get_object_or_404(AutoSearch, slug=self.kwargs['slug'])
        if self.request.user.is_authenticated:
            watched_list = WatchCars.objects.filter(user=self.request.user, active=True, car=car_obj).exists()
            data['watched'] = watched_list
        # liked = False
        # if likes_connected.likes.filter(id=self.request.user.id).exists():
        #     liked = True
        # data['number_of_likes'] = likes_connected.like_counts()
        # data['liked'] = liked
        return data



car_detail_view = CarDetailView.as_view()
