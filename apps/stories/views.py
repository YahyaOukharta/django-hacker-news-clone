import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StoryForm, CommentForm
from .models import Story, Vote, Comment

# pages
def frontpage(request):
    since = datetime.datetime.now() - datetime.timedelta(days=1)
    stories = Story.objects.filter(created_at__gte=since).order_by('-number_of_votes')[:30]
    return render(request, 'stories/frontpage.html',{'stories': stories})

def latest(request):
    stories = Story.objects.all()[:200]
    return render(request, 'stories/latest.html',{'stories': stories})

def search(request):
    query = request.GET.get('query')

    if (len(query)):
        stories = Story.objects.filter(title__icontains=query)
    else:
        stories = []
    return render(request, 'stories/search.html',{'stories': stories})


def detail(request,story_id):
    story = get_object_or_404(Story,pk=story_id)

    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.created_by = request.user
            comment.save()
            return redirect('detail',story_id=story_id)
    else:
        form = CommentForm()

    return render(request, 'stories/detail.html',{'story': story, 'form':form})


@login_required()
def vote(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    if story.created_by != request.user \
    and not Vote.objects.filter(created_by=request.user, story=story):
        vote = Vote.objects.create(story=story,created_by=request.user)
    
    next_page = request.GET.get('next_page','')
    if next_page == 'story':
        return redirect('detail',story_id=story_id)
    return redirect('frontpage')

@login_required()
def submit(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.created_by = request.user
            story.save()
            return redirect('frontpage')
    else:
        form = StoryForm()
    return render(request, 'stories/submit.html',{'form':form})
