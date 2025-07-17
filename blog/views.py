from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (ListView, 
	                               DetailView, 
	                                 CreateView,
	                                  UpdateView,
	                                   DeleteView)
from .models import post, Comment
from .forms import CommentForm

def home(request):
	context = {
		'posts': post.objects.all()
	}
	return render(request,'blog/home.html',context)

class PostListView(ListView):
	model = post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = post
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comments'] = self.object.comments.all()
		context['comment_form'] = CommentForm()
		return context
	
class PostCreateView(LoginRequiredMixin, CreateView):
	model = post
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = post
	fields = ['title','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = post
	success_url = '/'
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

@login_required
def add_comment(request, pk):
	post_obj = get_object_or_404(post, pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post_obj
			comment.author = request.user
			comment.save()
			messages.success(request, 'Your comment has been added!')
			return redirect('post-detail', pk=post_obj.pk)
	return redirect('post-detail', pk=post_obj.pk)

@login_required
def delete_comment(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	post_pk = comment.post.pk
	if request.user == comment.author:
		comment.delete()
		messages.success(request, 'Your comment has been deleted!')
	else:
		messages.error(request, 'You can only delete your own comments!')
	return redirect('post-detail', pk=post_pk)
		
def about(request):
	return render(request, 'blog/about.html',{'title':'About'})
