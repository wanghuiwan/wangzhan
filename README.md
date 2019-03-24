# wangzhan
#让django 知道如何修改数据库存储models里的class
#python3 manage.py makemigrations myhome
#让django 帮我们修改数据库
#python3 manage.py migrate


#django shell 用法  查询models中模型存储的数据
python3 manage.py shell
from myhome.models import Topic
Topic.objects.all()
查询数据全部数据进行循环
topics = Topic.objects.all()
for topic in topics:
    print (topic.id,topic)

查询制定数据
t = Topic.objects.get(id = 1)
t.text
t.date_added
看到关联数据   关联模型的小写加下划线加set  来获取 关联模型的关联数据。
topics.entry_set.all()












