import string
import secrets
from itertools import count

from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, AccountForm
from .models import Account
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "vault/home.html")

def register_view(request) -> HttpResponse:
    """Страница регистрации нового пользователя.

    GET  — показываем пустую форму.
    POST — валидируем форму, создаём пользователя, сразу логиним его
           и отправляем на список учётных записей.
    """
    # if request.user.is_authenticated:
    #     return redirect("/")  # пока account_list не написан

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else: # if request.method == "GET":
        form = RegisterForm()

    context = {"form": form}
    return render(request, template_name="vault/register.html", context=context)


def login_view(request):
    """
    Кастомная страница аутентификации
    GET - показываем форму с полями логин и пароль
    POST - пробуем войти: при успехе - входим в систему и редиректим на список учетных записей (главную страницу)

    """
    # if request.user.is_authenticated:
    #     return redirect("/")  # пока account_list не написан


    if request.method == "POST":
        # Считываем введенные значения из формы
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # authenticate - проверяет логин/пароль и возвращает User или None
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login - сохраняет пользователя в сессии
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('/')

        error = "Неверный логин или пароль"
    error = None
    return render(request, template_name="vault/login.html", context={"errors": error})


@require_http_methods(["POST"])
def logout_view(request):
    """
    Выход из системы
    """
    logout(request)
    return redirect('login')

@login_required
def todo_list_view(request):
    """
    Страница со списком учетных записей
    """
    accounts = Account.objects.filter(owner=request.user)
    paginator = Paginator(accounts, per_page=3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    count = accounts.count()

    context = {"accounts": page_obj, "count": count}
    return render(request, template_name="vault/todo_list.html", context=context)

@login_required
def todo_create_view(request):
    """Добавление новой учетной записи"""
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            # commit=False создаем объект, но пока не сохраняем в БД
            account = form.save(commit=False)
            # привязываем учетную запись к текущему пользователю
            account.owner = request.user
            account.save()
            return redirect('todo_list')
    form = AccountForm()

    context = {"form": form}
    return render(request, template_name="vault/todo_form.html", context=context)

@login_required
def todo_detail_view(request, pk):
    account = Account.objects.filter(pk=pk).first()
    context = {"account": account}
    return render(request,
                  template_name="vault/todo_detail.html",
                  context=context)

@login_required
def todo_edit_view(request, pk):
    # Получаем аккаунт, принадлежащий пользователю, или 404
    account = get_object_or_404(Account, pk=pk, owner=request.user)
    if request.method == "POST":
        #, Заполняем форму данными полученного аккаунта
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect("todo_detail", pk=account.pk)
    else:
        form= AccountForm(instance=account)

    return render(request,
                  template_name="vault/todo_form.html",
                  context= {"form": form}
                  )

@login_required
def todo_delete_view(request, pk):
    """
    GET - показываем страницу с подтверждением удаления
    POST - удаляем запись и возвращаемся на страницу списка учеток
    """
    account = get_object_or_404(Account, pk=pk, owner=request.user)
    if request.method == "POST":
        account.delete()
        return redirect('todo_list')
    return render(request, template_name="vault/todo_confirm_delete.html", context={"account": account})







def about(request):
    return render(request, "vault/about.html")

