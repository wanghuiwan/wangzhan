from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import TopicForm, EntryForm
from .models import Topic,Entry
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,Http404
# Create your views here.


def index(request):
    """学习笔记首页"""
    return render(request, 'myhome/index.html')


@login_required
def topics(request):
    """查看所有主题"""
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'myhome/topics.html', context)


@login_required
def topic(request,topic_id):
    """查看单个主题"""
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前登录的用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'myhome/topic.html', context)


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        # is_valid 校验数据是否符合标准
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            #保存数据
            form.save()
            '''重定向以及重定向地址获取'''
            return HttpResponseRedirect(reverse('myhome:topics'))
    context = {'form': form}
    #render 渲染页面
    return render(request, 'myhome/new_topic.html', context)


@login_required
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


@login_required
def edit_entry(request,entry_id):
    """编辑现有的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确认请求的主题属于当前登录的用户
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 初次请求，使用现有的条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            new_entry.save()
            '''重定向以及重定向地址定义'''
            return HttpResponseRedirect(reverse('myhome:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'myhome/edit_entry.html', context)



