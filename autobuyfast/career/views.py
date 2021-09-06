try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

import datetime

from category.models import Category, Tag
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import BadHeaderError, EmailMessage, send_mail, send_mass_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.db.models import Count, F, Q, Sum
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView
# from angalabiri.blog.forms import CommentForm
from next_prev import next_in_order, prev_in_order

from autobuyfast.core.forms import ContactForm, EmailSubscribeForm

# from .forms import EmailPostForm
from .models import Career, CareerApply

User = get_user_model()

# Create your views here.
class CareerListView(ListView):
    model = Career
    template_name = "career/list.html"
    ordering = ["title", "-pub_date"]
    queryset = Career.objects.filter(status="published")
    context_object_name = "careers"
    allow_empty = True
    paginate_by = 20
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        return Career.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        ).distinct()


career_view = CareerListView.as_view()

class CareerApplyView(SuccessMessageMixin, CreateView):
    model = Career
    template_name = "career/detail.html"
    ordering = ["title", "-pub_date"]
    context_object_name = "career"
    slug_field = "slug"
    slug_url_kwarg = "slug"

career_detail_view = CareerApplyView.as_view()

