from django.contrib import admin

from django.contrib import admin
from .models import User, Post,Like

class UserAdmin(admin.ModelAdmin):
    model=User
    list_display=['username','email','mobile','address']
admin.site.register(User,UserAdmin)


class PostAdmin(admin.ModelAdmin):
    model=Post
    list_display=['title','description','content','creation_date','owner','is_public']
admin.site.register(Post,PostAdmin)

class LikeAdmin(admin.ModelAdmin):
    model=Like
    list_display=['post','user']
admin.site.register(Like,LikeAdmin)
