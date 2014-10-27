from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from dajaxice.decorators import dajaxice_register
from .models import Needed, UserProfile
from .forms import NeededForm, UserForm, UserProfileForm


# Create your views here.
def didDownvote(user, needed):
    dvoted = False
    for u in needed.downvoted_by.all():
        if u == user:
            dvoted = True
            return True
    if dvoted == False:
        return False
        
    

def addlikes(amount, needed):
    needed.likes = needed.likes + amount


def index(request):
    context = RequestContext(request)
   
    items = Needed.objects.order_by('-likes', '-posted')
    
    item_list_no_score = Needed.objects.all()
   
   
    for n in items:
        n.url = n.title.replace(' ', '_')
        n.url = n.url
    context_dict = {'items':items}
    return render_to_response('index.html', context_dict, context)
@login_required
def add_needed(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        form = NeededForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            pass
    else:
        form = NeededForm()
        
    
    return render_to_response('add_needed.html', {'form': form}, context)
    
def register(request):
    context = RequestContext(request)
    
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            registered = True
            
        else:
            print user_form.errors, profile_form.errors
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render_to_response('register.html', {'user_form': user_form, 'profile_form':profile_form, 'registered':registered}, context)
        
        
def user_login(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Your account has been disabled!')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied")
        
    else:
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    
    return HttpResponseRedirect('/')
    

def detail(request, needed_title_url):
    context = RequestContext(request)
    
    needed_name = needed_title_url.replace('_', ' ')
    
   
    context_dict = {'needed_name': needed_name, 'needed_title_url': needed_title_url}
    try:
        needed = Needed.objects.get(title=needed_name)
        context_dict['needed'] = needed
        
    except:
        pass
    
    return render_to_response('needed.html', context_dict, context)

@login_required

def vote(request, needed_title_url):
    
    needed_name = needed_title_url.replace('_', ' ')
    user_liked = False
    try:
        selected_choice = get_object_or_404(Needed, title=needed_name)
    
    except (KeyError, Needed.DoesNotExist):
        
        return HttpResponseRedirect('/needed/%s' % needed_title_url)
        
    else:
        for user in selected_choice.liked_by.all():
            if user == request.user:
                user_liked = True
                
        if user_liked == False:
        
            selected_choice.likes += 1
            selected_choice.save()
            selected_choice.liked_by.add(request.user)
                
        return HttpResponseRedirect('/needed/%s' % needed_title_url)
        
        
   
def userPage(request, user_url):
    context = RequestContext(request)
    
    username = user_url
    context_dict = {}
    try:
        realUser = User.objects.get(username=username)
        context_dict['realUser'] = realUser
        
    
        userP = UserProfile.objects.get(user=realUser)
        
        context_dict['userP'] = userP
    
    except:
        return HttpResponse('No such user exist!')
    else:
       
        return render_to_response('userPage.html', context_dict, context)
def aboutus(request):
    context = RequestContext(request)
    context_dict = {}
    
    return render_to_response('about.html', context_dict, context)