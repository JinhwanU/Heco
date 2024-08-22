from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import TemplateView
from common.forms import UserForm

#로그인 정보 화면에 전달
from django.contrib.auth.views import LoginView
# Create your views here.


class HomeView(TemplateView):
    template_name = "partials/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_list"] = ["lists"]
        return context


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse("common:login"))
    else:
        form = UserForm()
    return render(request, "account/signup.html", {"form": form})


class UserProfileView():
    pass

#로그인 성공시 세션 데이터 
class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        # 로그인 성공 후 세션에 데이터 저장
        self.request.session['user_id'] = user.id
        self.request.session['username'] = user.username
        
        return redirect('board:post_list')
