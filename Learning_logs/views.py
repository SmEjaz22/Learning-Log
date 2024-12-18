from django.shortcuts import render, redirect, get_object_or_404
from .models import topic_ofinterest, Entry

from .forms import TopicForm, EntryForm

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone
from django.views.decorators.cache import never_cache
# Create your views here.

def index(request):
    """Home page for LLog"""
    return render(request,'Learning_logs/index.html')
#  When a URL request matches the pattern we just defined,
# Django looks for a function called index() in the views.py file.
# Django then passes the request object to this view function.
# In this case, we don’t need to process any data for the page,
# so the only code in the function is a call to render().

# The render() function here passes two arguments: the original request object
# and a template it can use to build the page.

@login_required # TO make it work add login_url in settings
@never_cache
def topics(request):
    """Show all topics."""
    # topics = topic_ofinterest.objects.order_by('date_modified') # date_modified is a variable defined in models.py
    
    topics = topic_ofinterest.objects.filter(owner=request.user).order_by('date_modified') #to restrict each topic to individual user
    
    context = {'topics': topics} # A context is a dictionary in which 
    # the keys are names we’ll use in the template to access the data we want,
    # and the values are the data we need to send to the template.
    return render(request, 'Learning_logs/topics.html', context)
#request object, the template we want to use, and the context dictionary

@login_required # TO make it work add login_url in settings
@never_cache
def topic(request,topic_id_from_url):
    """Show a single topic and all its entries."""
    try:
        topic=topic_ofinterest.objects.get(id=topic_id_from_url)
    
    
    except topic_ofinterest.DoesNotExist:
        raise Http404("404 not found")
    
    
    
    
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404 
    
    entries=topic.entry_set.order_by('-date_added')# minus sign display the most recent entries first.
    context={'topic': topic, 'entries':entries}
    return render(request,'Learning_logs/topic.html',context)


# CHapter 19
@login_required # TO make it work add login_url in settings
@never_cache
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            
            form.save()
            return redirect('Learning_logs:topics')
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'Learning_logs/new_topic.html', context)

@login_required # TO make it work add login_url in settings
@never_cache
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = topic_ofinterest.objects.get(id=topic_id)
    
    
        # Make sure the topic's entry belongs to the current user. TIY 19_4
    if topic.owner != request.user:
        print("get the hell outta here")
        raise Http404 
    
    
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('Learning_logs:topic', topic_id_from_url=topic_id)
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'Learning_logs/new_entry.html', context)


@login_required # TO make it work add login_url in settings
@never_cache
def edit_entry(request, entry_id):
    
    """Edit an existing entry."""
    try:
        entry = Entry.objects.get(id=entry_id)
        topic = entry.topic
    except Entry.DoesNotExist:
        raise Http404("You do not have permission to edit this entry")
        
    
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            if form.has_changed():  # Check if any fields were actually changed
                entry.last_modified = timezone.now()  # Update only if changes were made
            form.save()
            return redirect('Learning_logs:topic', topic_id_from_url=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'Learning_logs/edit_entry.html', context)

@login_required
@never_cache
def entry_versions(request, entry_id):
 # Get the current main entry
    try:
        entry = Entry.objects.get(pk=entry_id)
    except Entry.DoesNotExist:
        raise Http404("The entry you are looking for does not exist.")
    
    topic = entry.topic


    if topic.owner != request.user:
        raise Http404
    # Get past versions, excluding the current main entry
    past_entries = entry.history.all().order_by('-date_created')

    return render(request, 'Learning_logs/entry_versions.html', {
        'entry': entry,
        'past_entries': past_entries,
        'topic':topic
    })

def delete_topic(request,topic_id_from_url):
    """Delete a topic."""
    try:
        topic = topic_ofinterest.objects.get(id=topic_id_from_url)
    except topic_ofinterest.DoesNotExist:
        raise Http404("Topic not found")

    # Make sure the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404("You do not have permission to delete this topic")

    topic.delete()
    return redirect('Learning_logs:topics')