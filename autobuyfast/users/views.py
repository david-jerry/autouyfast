from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import BadHeaderError, EmailMessage, send_mail, send_mass_mail
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)

from autobuyfast.cars.models import AutoSearch, Image, WatchCars
from autobuyfast.users.forms import CarRequestForm

from .forms import (
    AlertSettingsForm,
    BuyerForm,
    BuyerProfileForm,
    SellerForm,
    SellerProfileForm,
    TestimonyForm,
)
from .models import AlertSetting, CarRequest, Profile, Testimonial

User = get_user_model()


class SavedCars(LoginRequiredMixin, ListView):
    model = WatchCars
    template_name = "users/saved_cars.html"
    ordering = ["-car", "-created"]
    page_kwarg = 'page'
    paginate_by = 20
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = WatchCars.objects.all().filter(user=self.request.user)
        return context
    

class CarAdListView(LoginRequiredMixin, ListView):
    model = AutoSearch
    template_name = "users/car_ads.html"
    ordering = ["title", "-created"]
    page_kwarg = 'page'
    paginate_by = 40
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = AutoSearch.objects.all().filter(dealer=self.request.user)
        return context






# Default user type creation views
class SellerCreateView(SuccessMessageMixin, SignupView):
    template_name = "account/signup_seller.html"
    success_url = reverse_lazy("account_login")
    success_message = _("Your seller account have been created, Please confirm your email")
    form_class = SellerForm

seller_signup = SellerCreateView.as_view()


class BuyerCreateView(SuccessMessageMixin, SignupView):
    template_name = "account/signup_buyer.html"
    success_url = reverse_lazy("account_login")
    success_message = _("Your buyer account have been created, Please confirm your email")
    form_class = BuyerForm

buyer_signup = BuyerCreateView.as_view()





# Default user views for update and detail

class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cars = WatchCars.objects.all().filter(user=self.request.user)
        context["cars"] = cars.order_by("-created")[:5]
        context["cars_count"] = cars.count()
        return context
    

user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["first_name", "last_name", "email", "phone_no"]
    success_message = _("Your personal information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()









# Update views for buyer profile and seller profiles

class UserSellerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Profile
    fields = [
            "profile_display",
            "banner_display",
            "dealership_name",
            "bio",
            "website",
            "country",
            "address",
            "city",
            "zipcode",
            "security_quest",
            "security_answer"
        ]
    success_message = "You have successfully updated your profile."
    template_name = "users/seller_update.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]


seller_update_view = UserSellerUpdateView.as_view()

def car_request_view(request):
    
    if request.method == "POST":
        form = CarRequestForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data['email']
            date = form.cleaned_data['pickup']
            service = form.cleaned_data["services"]
            message = form.cleaned_data["message"]
            form.save()
            send_mail("Delivery Request", f"{name} made a request for {service} set to be delivered on this day: {date}.\n \n Further information for this request is: {message}. \n Tracking number will be sent to you after a follow up email has been sent.", "info@autobuyfast.com", ['info@autobuyfast.com', email], fail_silently=False)
            messages.success(request, "Your request has been sent successfuly")
            return HttpResponseRedirect(reverse("home"))
    
    else:
        form = CarRequestForm()

    return render(request, 'pages/about.html', {'request_form': form})
    


class UserBuyerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Profile
    fields = [
            "profile_display",
            "country",
            "address",
            "city",
            "zipcode",
            "security_quest",
            "security_answer"
        ]
    success_message = "You have successfully updated your profile."
    template_name = "users/buyer_update.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]


buyer_update_view = UserBuyerUpdateView.as_view()









# User testimony view

class TestimonyView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Testimonial
    form_class = TestimonyForm
    success_message = "Thank you for your review of our service, this will enable us improve to serve you even better."
    template_name = "users/testimony.html"

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def form_valid(self, form):
        form.instance.user = self.request.user
        User.objects.filter(username=self.request.user.username).update(has_testified=True)
        form.instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["testimony_form"] = self.form_class
        return context

testimony_create_view = TestimonyView.as_view()










# User notification alert settings

class NotificationSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = [
            "newsletter_notif", 
            "car_sold_notif", 
            "car_price_notif"
        ]
    success_message = "You have successfully updated your notification settings."
    template_name = "users/notification_setting.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]


notification_setting_view = NotificationSettingsView.as_view()
