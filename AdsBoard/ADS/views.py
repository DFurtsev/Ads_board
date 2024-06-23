from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from .filters import AdFilter
from .forms import AdForm, ResponseForm
from .models import *


class AdsList(ListView):
    model = Ad
    ordering = '-publication_time'
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 10


class MyAds(AdsList):
    def get_queryset(self):
        user = self.request.user
        queryset = Ad.objects.filter(author=user).order_by('-publication_time')
        return queryset
    context_object_name = 'myads'
    template_name = 'my_ads.html'
    paginate_by = 10


class Responses(ListView):
    model = Response
    #ordering = '-time'
    template_name = 'responses.html'
    context_object_name = 'responses_to_me'
    paginate_by = 10

    def get_queryset(self):
        user_responses = Response.objects.filter(ad__author_id=self.request.user.id)
        active_responses = user_responses.filter(is_active=True)
        self.filterset = AdFilter(self.request.GET, queryset=active_responses.order_by('-time'), request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Response.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def post(self, request, *args, **kwargs):
        if 'pk' in request.POST:
            response = Response.objects.get(id=request.POST['pk'])
            response.is_active = False
            response.save()
        else:
            return render(self.request, '403.html')
        return redirect('responses_for_me')



class RejectResponses(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('ADS.delete_response')
    raise_exception = True
    model = Response
    success_url = reverse_lazy('responses_for_me')
    template_name = 'reject_response.html'



class AdDetail(FormMixin, DetailView):
    model = Ad
    template_name = 'ad.html'
    raise_exception = True
    context_object_name = 'ad'
    queryset = Ad.objects.all()
    form_class = ResponseForm

    def post(self, *args, **kwargs):
        form = ResponseForm(self.request.POST or None)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = Ad.objects.get(id=self.kwargs['pk'])
            response.user = self.request.user
            response.save()
            return super().form_valid(form)
            
    def get_success_url(self, **kwargs):
        return reverse_lazy('ads')


class AdCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('ADS.add_ad')
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'ad_create.html'

    def form_valid(self, form):
        current_user = self.request.user.id
        ad = form.save(commit=False)
        ad.author = User.objects.get(id=current_user)
        ad.save()
        return super().form_valid(form)


class AdUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('ADS.change_ad')
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'


class ConfirmEmail(UpdateView):
    model = User
    context_object_name = 'confirm_user_email'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'account/invalid_code.html')
        return redirect('account_login')


class SendDistribution(CreateView):
    template_name = '403'

