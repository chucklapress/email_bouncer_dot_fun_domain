from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from email_parser.forms import EmailForm
from email_parser.models import dmarc_check
from email_parser.forms import dmarc_checkForm


class dmarcListView(ListView):
    model = dmarc_check
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class IndexView(TemplateView):
    template_name = "index.html"

class dmarc_checkView(TemplateView):

    template_name = 'index1.html'

    def get_context_data(self, **kwargs):
        context = super(dmarc_checkView, self).get_context_data(**kwargs)
        context['line'] = dmarc_check.objects.all().order_by('-id')[0:1]
        context['form'] = dmarc_checkForm()
        return context

        form = dmarc_checkForm(request.POST)
        if form.is_valid():
            form.save()

def email(request):
    if request.method == 'GET':
        form = EmailForm()
    else:
        form = EmailForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            subject = form.cleaned_data['subject']
            return_from = form.cleaned_data['return_from']
            the_dmarc_check = form.cleaned_data['the_dmarc_check']
            try:
                send_mail(subject, the_dmarc_check, return_from, [address])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('/')
    return render(request, "email_parser/email.html", {'form': form})

def thanks(request):
    return HttpResponse('Thank you for your message.')
