from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import User, Post, Response
from .filters import PostFilter
from .forms import PostForm, ResponseForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .signals import notify_about_accept_response


class PostsList(ListView):
    model = Post
    ordering = '-datetime_in'
    context_object_name = 'post'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_template_names(self):
        if self.request.path == '/board/search/':
            return 'search.html'
        return 'board.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'ad.html'
    context_object_name = "post"


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'ad_edit.html'

    def form_valid(self, form):
        pos = form.save(commit=False)
        pos.author = self.request.user
        pos.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'ad_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_post',)
    model = Post
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('post_list')


class ResponseList(ListView):
    model = Response
    ordering = '-time_response'
    template_name = 'response.html'
    context_object_name = "response"
    paginate_by = 10


class ResponseCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_response',)
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'
    success_url = reverse_lazy('response_list')

    def form_valid(self, form):
        res = form.save(commit=False)
        res.user = self.request.user
        res.post_id = self.kwargs['pk']
        res.save()
        return super().form_valid(form)


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_response',)
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('Response_list')


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'users/invalid_code.html')
            return redirect('account_login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


@login_required
def response_accept(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.condition = True
        response.save()
        notify_about_accept_response(response_id=response.id)
        return HttpResponseRedirect('/board/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


@login_required
def response_delete(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.delete()
        return HttpResponseRedirect('/board/responses')
    else:
        return HttpResponseRedirect('/accounts/login')
