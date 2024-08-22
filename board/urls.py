from django.urls import path
from . import views

#게시판 API post
app_name = 'board'

urlpatterns = [
     #게시판
     path('', views.post_list, name='post_list'),                                  #게시판 전체 조회
     path('<int:category>', views.category_post_list, name='category_post_list'),  #게시판 카테고리 조회
     path('create_page/', views.create_page, name='create_page'),                  #게시글 작성 페이지 이동 
     path('post_detail/<int:post_id>', views.post_detail, name='post_detail'),     #게시글 상세 조회
     path('create/', views.post_create, name='post_create'),                       #게시글 작성
     path('delete/<int:post_id>', views.post_delete, name="post_delete"),          #게시글 삭제 
     path('update_page/<int:post_id>', views.update_page, name="update_page"),     #게시물 update 페이지 이동 
     path('update/<int:post_id>/', views.update, name='update'),                  #게시물 update

     #댓글 
     path('comment_create/<int:post_id>', views.comment_create, name="comment_create"),
     path('comment_delete/<int:comment_id>', views.comment_delete, name="comment_delete"),
]
