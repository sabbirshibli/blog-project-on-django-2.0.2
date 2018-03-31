<a href="/posts/{{ obj.id }}/">{{ obj.title }}</a><br> -->
<a href='{% url "posts:detail" id=obj.id %}'>{{ obj.title }}</a><br>
