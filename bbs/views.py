from django.shortcuts import render

from django.views import View

from django.http.response import JsonResponse
from django.template.loader import render_to_string

from .models import Topic
from .forms import TopicForm,TopicFirstForm


import time

class IndexView(View):
    
    def render_content(self,request):
        topics          = Topic.objects.order_by("-dt")
        context         = { "topics":topics }

        return render_to_string("bbs/content.html",context,request)

    def get(self, request, *args, **kwargs):

        topics  = Topic.objects.order_by("-dt")
        context = { "topics":topics }

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        data    = { "error":True }
        form    = TopicForm(request.POST)

        if not form.is_valid():
            print(form.errors)
            return JsonResponse(data)

        form.save()

        data["error"]   = False
        data["content"] = self.render_content(request)

        return JsonResponse(data)

    def delete(self, request, *args, **kwargs):
        
        data    = { "error":True }

        if "pk" not in kwargs:
            return JsonResponse(data)

        topic   = Topic.objects.filter(id=kwargs["pk"]).first()

        if not topic:
            return JsonResponse(data)

        topic.delete()

        data["error"]   = False
        data["content"] = self.render_content(request)

        return JsonResponse(data)

index   = IndexView.as_view()


# ロングポーリング
class RefreshView(View):

    def get(self, request, *args, **kwargs):

        data    = { "error":True }

        form    = TopicFirstForm(request.GET)
        
        #XXX:誰も何も投稿していない場合、firstに来る値は何もないので、必ずバリデーションエラーになってしまう。
        #未投稿の状況でもロングポーリングをさせるには、nullを許可する必要が有ると思われる。
        if not form.is_valid():
            print(form.errors)
            return JsonResponse(data)

        cleaned         = form.clean()

        first_id        = None
        if "first" in cleaned:
            first_id    = cleaned["first"]


        #30回ループする。(1秒おきにDBにアクセスする)
        #CHECK:このループは最大で30秒間レスポンスを返さないことを意味しているので、ブラウザのタイムアウトを考慮して調整する必要が有る。
        for i in range(30):

            topic   = Topic.objects.order_by("-dt").first()

            #topicが存在しており、そのtopicがかつての最新のものと違う場合、ループを抜ける。
            if topic:
                if topic.id != first_id:
                    break
            else:
                #かつての最新の投稿がNoneではない場合、削除されたことを意味するので、この場合もループを抜ける
                if first_id != None:
                    break

            time.sleep(1)
            #print("ロングポーリング中")


        topics  = Topic.objects.order_by("-dt")
        context = { "topics":topics }

        data["error"]   = False
        data["content"] = render_to_string("bbs/content.html",context,request)

        return JsonResponse(data)

refresh = RefreshView.as_view()


