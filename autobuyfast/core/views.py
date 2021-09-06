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

from autobuyfast.core.forms import ContactForm, EmailSubscribeForm

# from .forms import EmailPostForm
from .models import EmailSubscribe, Faq  # , Comment

# from angalabiri.blog.forms import CommentForm



User = get_user_model()

# Create your views here.
class FaqListView(ListView):
    model = Faq
    template_name = "pages/faq.html"
    ordering = ["title", "-created"]
    queryset = Faq.objects.all_faq()
    context_object_name = "faqs"
    allow_empty = True
    paginate_by = 5

faq_view = FaqListView.as_view()

def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']

            try:
                send_mail(subject, message, from_email, ['info@bizwallet.org'], fail_silently=False)
                messages.success(request, "Your Email Has been sent successfuly")
            except BadHeaderError:
                messages.error(request, "There was an error sending yout email at the moment, please try again later.")
                # return HttpResponse('Invalid Header found')
            return redirect('home')
    return render(request, 'pages/contact.html', {'form': form})



class UserEmailSubscribe(SuccessMessageMixin, CreateView):

    model = EmailSubscribe
    template_name = "snippets/footer.html"
    form_class = EmailSubscribeForm
    success_url = reverse_lazy("home")
    success_message = _("Email successfully added to our email list")

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.user = self.request.user
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())

email_subscribe = UserEmailSubscribe.as_view()


    