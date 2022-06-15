from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import NewsStory
from .forms import StoryForm


class IndexView(generic.ListView):
    template_name = 'news/index.html'

    def get_queryset(self):
        '''Return all news stories.'''
        return NewsStory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_filter'] = get_user_model().objects.all()
        context['latest_stories'] = NewsStory.objects.all().order_by('-pub_date')[:4]
        context['all_stories'] = NewsStory.objects.all().order_by('-pub_date')
        return context

class StoryView(generic.DetailView):
    model = NewsStory
    template_name = 'news/story.html'
    context_object_name = 'story'
    
class AuthorView(generic.DetailView):
    template_name = 'news/author.html'
    context_object_name = 'author'
    
    def get_context_data(self, **kwargs):
        context = super(AuthorView, self).get_context_data(**kwargs)
        context['author'] = NewsStory.objects.all()
        return context

    def get_queryset(self):
        author = get_user_model().objects.filter(self.kwargs['pk'])
        return NewsStory.objects.filter(author = author)

class AddStoryView(generic.CreateView):
    form_class = StoryForm
    context_object_name = 'storyForm'
    template_name = 'news/createStory.html'
    success_url = reverse_lazy('news:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # def get_author_name(self, **kwargs):
    #     user = self.get_object(pk)
    #     context = {}
    #     context['latest_stories'] = NewsStory.objects.all().filter(author=user)[:4]
    #     context['all_stories'] = NewsStory.objects.all().filter(author=user).all()
    #     return context
