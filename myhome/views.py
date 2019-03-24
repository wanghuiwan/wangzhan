from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import TopicForm, EntryForm
from .models import Topic
# Create your views here.


def index(request):
    """学习笔记首页"""
    return render(request, 'myhome/index.html')


def topics(request):
    """查看所有主题"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'myhome/topics.html', context)


def topic(request,topic_id):
    """查看单个主题"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'myhome/topic.html', context)


def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            '''重定向以及重定向地址定义'''
            return HttpResponseRedirect(reverse('myhome:topics'))
    context = {'form': form}
    return render(request, 'myhome/new_topic.html', context)


def new_entry(request, topic_id):
    """添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # 未提交数据时创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry= form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            '''重定向以及重定向地址定义'''
            return HttpResponseRedirect(reverse('myhome:topic', args=[topic_id]))
        context = {'topic': topic, 'form': form}
        return render(request, 'myhome/new_entry.html', context)





