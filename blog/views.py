# from django.shortcuts import render, get_object_or_404
# from .models import Post
# from .form import PostForm
# from django.shortcuts import redirect

# # Create your views here.
# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'blog/post_list.html', {
#         'posts': posts
#     })

# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post_details.html', {
#         'post': post
#     })
    
# def post_create(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('blog:post_detail', slug=post.slug)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_form.html', {
#         'form': form
#     })


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .form import PostForm
from django.views.generic.edit import FormView
from .form import RegisterForm
from django.contrib.auth import login
from django.shortcuts import redirect

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs = {'slug': self.object.slug})

class PostUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        from django.contrib import messages
        messages.error(self.request, 'You do not have permission to edit this post.')
        
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs = {'slug': self.object.slug})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
class PostPublishView(LoginRequiredMixin, UpdateView):
    model = Post
    permission_required = 'blog.can_publish_post'
    raise_exception = True
    template_name = 'blog/post_confirm_publish.html'
    fields = ['is_published']
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs = {'slug': self.object.slug}) 
    
class RegisterFormView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
        
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:post_list')
        return super().dispatch(request, *args, **kwargs)