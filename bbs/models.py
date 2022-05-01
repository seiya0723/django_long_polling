from django.db import models
from django.utils import timezone

class Topic(models.Model):
    
    #ロングポーリングを実現させるためには、order_byは必須。並び替えを機能させるために、投稿日時を記録するフィールドを追加しておく。

    dt      = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    comment = models.CharField(verbose_name="コメント",max_length=2000)

    def __str__(self):
        return self.comment
