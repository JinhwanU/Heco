from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from board.models import Category, Posts, Comments

import boto3
from botocore.exceptions import NoCredentialsError
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
import requests
import openai

from django.core.paginator import Paginator

#게시글 전체 조회
def post_list(request):
    #user = User()
    #로그인 후 받아오는 방법 고민
    user_id = request.session.get('user_id')
    user_username =request.session.get('username')
    posts = Posts.objects.all()

    paginator = Paginator(posts, 9)  # 한 페이지에 9개
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'id' : user_id,
        'username' : user_username,
        }
    return render(request, 'board/post_list.html', context)


#게시글 카테고리 조회
def category_post_list(request, category):
    errMessage = {"err" : '게기글 조회 오류 발생으로 다시 조회 부탁드립니다.'}
    if request.method == 'GET':
        posts = Posts.objects.filter(category=category)
        id = request.GET.get('id')
        username = request.GET.get('username')

        paginator = Paginator(posts, 9)  # 한 페이지에 9개
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'category': category,
            'id' : id,
            'username' : username,
            } 
        return render(request, 'board/category_post_list.html', context)
    return render(request, 'board/category_post_list.html', errMessage)


#게시글 상세 조회[게시글 username 가져와야함] 
def post_detail(request, post_id):
    #로그인 한 user
    id = request.GET.get('id')
    username = request.GET.get('username')
    #게시물 데이터
    post = get_object_or_404(Posts, id=post_id)
    #댓글 데이터
    comments = Comments.objects.filter(post_id=post_id)

    context = {
        'post': post,
        'comments' : comments,
        'id'  : id, 
        'username' : username,
    }
    return render(request, 'board/post_detail.html', context)

#게시글 작성 페이지 이동
def create_page(request):
    id = request.GET.get('id')
    username = request.GET.get('username')
    context = {
        'id' : id, 
        'username' : username,
    }
    return render(request, 'board/post_create.html', context)


#게시글 작성
def post_create(request):
    if request.method == 'POST':
        #게시판
        post = Posts()
        post.title = request.POST['title']
        post.contents = request.POST['contents']
        post.image_url = upload_to_aws(request.FILES['image']) #AWS S3 연결 
        post.category = request.POST['category']
        #user 데이터 가져올수 있는지 확인
        user = User.objects.get(id=request.POST['id'])
        post.user_id = user
        #저장(insert)
        post.save()
        
        #전체 게시글로 이동 
        #posts = Posts.objects.all()

        #context = {
        #    "posts": posts,
        #    "id" : request.POST['id'],
        #    "username" : request.POST['username']
        #}

        #글쓰기 성공시 이동 
        return redirect('board:post_list')
        #return render(request, 'board/post_list.html', context)  
    
    #글쓰기 실패시 이동
    return render(request, 'board/post_create.html', { })    



#게시글 수정 페이지 이동 
def update_page(request, post_id):
    post = get_object_or_404(Posts, id=post_id)    
    context = {
        'post' : post,
        'id' : request.GET.get('id'),
        'username' : request.GET.get('username'),
        }
    return render(request, 'board/post_update.html', context)

#게시글 수정
def update(request, post_id):
    post = Posts.objects.get(id=post_id)
    post.title = request.POST.get('title')
    post.contents = request.POST.get('contents')
    post.image_url = upload_to_aws(request.FILES['image']) #AWS S3 연결 
    # post.category = request.POST.get('category') #수정불가
    post.save()
    post = get_object_or_404(Posts, id=post_id)
    comments = Comments.objects.filter(post_id=post_id)
    context = {
        'post' : post,
        'comments' : comments,
        'id' : request.GET.get('id'),
        'username' : request.GET.get('username'),
        }
    return render(request, 'board/post_detail.html', context)
    

#게시글 삭제
def post_delete(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    post.delete()
    #posts = Posts.objects.all()
    #context = {
    #    'posts' : posts,
    #    'id' : request.GET.get('id'),
    #    'username' : request.GET.get('username')
    #}
    return redirect('board:post_list')
    #return render(request, 'board/post_list.html', context)
    
#댓글 생성 
def comment_create(request, post_id):
    #게시판 외래키, User 외래키 입력 
    post = Posts.objects.get(id=post_id)
    comment = Comments()
    comment.contents = request.POST['comment_content']
    user_id = request.POST.get('id')
    user_data = User.objects.get(id=user_id)  # id를 사용하여 UserData 인스턴스를 가져옴
    comment.user_id = user_data # 가져온 인스턴스를 할당
    comment.post_id = post
    #댓글 저장 
    comment.save()
    #댓글 조회
    comments = Comments.objects.filter(post_id=post_id)

    #댓글 저장 -> 게시판 상세 조회(게시글 데이터, 댓글 데이터)
    context = {
        'post':post,
        'comments' : comments,
        'id': request.GET.get('id'),
        'username': request.GET.get('username'),
    }

    return render(request, 'board/post_detail.html', context)


#댓글 삭제 
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    comment.delete()
    
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Posts, id=post_id)
    comments = Comments.objects.filter(post_id=post_id)

    context = {
        'post' : post,
        'comments' : comments,
        'id': request.GET.get('id'),
        'username': request.GET.get('username'),
    }
    return render(request, 'board/post_detail.html', context)
