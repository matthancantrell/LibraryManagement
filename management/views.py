from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import MyUser, Book, Img, Organization, Library
from django.urls import reverse
from management.utils import permission_check

#region Index
def index(request):
    user = request.user if request.user.is_authenticated else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)
#endregion

#region Signup
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)
#endregion

#region Login
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('view_organization_list'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('view_organization_list'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'view_organization_list',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)
#endregion

#region Logout
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))
#endregion

#region Set Password (Login Required)
@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)
#endregion

#region Add Book (Permission Required)
@user_passes_test(permission_check)
def add_book(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Book(
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                genre=request.POST.get('genre', ''),
                publish_date=request.POST.get('publish_date', '')
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_book',
        'state': state,
    }
    return render(request, 'management/add_book.html', content)
#endregion

#region Add Organization (Permission Required)
@user_passes_test(permission_check)
def add_org(request):
    user = request.user
    state = None

    if request.method == 'POST':
        new_organization = Organization(
            name=request.POST.get('name', ''),
            description=request.POST.get('description', '')
        )
        new_organization.save()
        state = 'success'

        cont = {
            'user': user,
            'state': state
        }

        return render(request, 'management/view_organization_list.html')

    content = {
        'user': user,
        'active_menu': 'view_organization_list',
        'state': state,
    }
    return render(request, 'management/add_org.html', content)
#endregion

def add_lib(request):
    state = None

    if request.method == 'POST':
        organization_id = request.POST.get('organization')
        organization = Organization.objects.get(pk=organization_id)

        new_library = Library(
            name=request.POST.get('name', ''),
            organization=organization
        )
        new_library.save()
        state = 'success'

    organizations = Organization.objects.all()

    content = {
        'state': state,
        'organizations': organizations,
    }
    return render(request, 'management/add_lib.html', content)

#region View Book List
def view_book_list(request):
    user = request.user if request.user.is_authenticated else None
    genre_list = Book.objects.values_list('genre', flat=True).distinct()
    query_genre = request.GET.get('genre', 'all')
    library_id = request.GET.get('id', '')

    library = Library.objects.get(pk=library_id)
    if (not query_genre) or Book.objects.filter(genre=query_genre).count() is 0:
        query_genre = 'all'
        book_list = Book.objects.filter(library=library)
    else:
        book_list = Book.objects.filter(genre=query_genre, library=library)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        book_list = Book.objects.filter(name__contains=keyword, library=library)
        query_genre = 'all'

    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_book',
        'genre_list': genre_list,
        'query_genre': query_genre,
        'book_list': book_list,
        'library_name': library.name,
        'library': library
    }
    return render(request, 'management/view_book_list.html', content)
#endregion

#region Organization List
def view_organization_list(request):
    organizations = Organization.objects.all()
    content = {
        'organization_list': organizations,
        'query_organization': request.GET.get('organization', None),
    }
    return render(request, 'management/view_organization_list.html', content)

#endregion

def organization_detail(request):
    user = request.user if request.user.is_authenticated else None
    organization_id = request.GET.get('id', '')
    if organization_id == '':
        return HttpResponseRedirect(reverse('view_organization_list'))
    try:
        organization = Organization.objects.get(pk=organization_id)
    except Organization.DoesNotExist:
        return HttpResponseRedirect(reverse('view_organization_list'))
    content = {
        'user': user,
        'active_menu': 'view_organization',
        'organization': organization,
        'organization_name': organization.name,
        'organization_description': organization.description
    }
    return render(request, 'management/organization_detail.html', content)

def library_detail(request):
    return render(request, 'management/view_book_list.html')

#region Detail
def detail(request):
    user = request.user if request.user.is_authenticated else None
    book_id = request.GET.get('id', '')
    if book_id == '':
        return HttpResponseRedirect(reverse('view_book_list'))
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return HttpResponseRedirect(reverse('view_book_list'))
    content = {
        'user': user,
        'active_menu': 'view_book',
        'book': book,
    }
    return render(request, 'management/detail.html', content)
#endregion

#region Add Image (Permission Required)
@user_passes_test(permission_check)
def add_img(request):
    user = request.user
    state = None
    if request.method == 'POST':
        try:
            new_img = Img(
                    name=request.POST.get('name', ''),
                    description=request.POST.get('description', ''),
                    img=request.FILES.get('img', ''),
                    book=Book.objects.get(pk=request.POST.get('book', ''))
            )
            new_img.save()
        except Book.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'state': state,
        'book_list': Book.objects.all(),
        'active_menu': 'add_img',
    }
    return render(request, 'management/add_img.html', content)
#endregion
