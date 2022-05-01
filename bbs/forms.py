from django import forms
from .models import Topic

class TopicForm(forms.ModelForm):

    class Meta:
        model   = Topic
        fields  = [ "comment" ]


#ロングポーリング用のフォームクラス
class TopicFirstForm(forms.Form):

    #Topicのidに基づく
    first   = forms.IntegerField(required=False)

