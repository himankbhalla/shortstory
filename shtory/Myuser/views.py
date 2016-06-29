from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from django.contrib.auth import login, logout
from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from Story.models import *
import json
from django.contrib import auth
from django.core.context_processors import csrf
#from social_auth.backends import get_backend
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
import datetime
#import feedparser
# Create your views here.

class UserCreationForm(forms.ModelForm):
	password1  = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, help_text = "Should be same as Password")

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = ''
		for field in self.fields:
			self.fields[field].required = True

	class Meta:
		model = CustomUser
		fields = ['username', 'email']
	def clean_passwd2(self):
		passwd1 = self.cleaned_data.get("passwd1")
		passwd2 = self.cleaned_data.get("passwd2")
		if passwd1 and passwd2 and passwd1 != passwd2:
			raise forms.ValidationError("Passwords don't match")
		return passwd2
	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit = False)
		user.set_password(self.cleaned_data["password1"])
		user.email = self.cleaned_data['email']
		if commit:
			user.is_active = False
			user.save()
		return user
	#clean email field
	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			CustomUser._default_manager.get(email=email)
		except CustomUser.DoesNotExist:
			return email
		raise forms.ValidationError('duplicate email')

class profileForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields =  ['username', 'email', 'gender', 'dob', 'phone_number','profile_pic']
		
		
class profile_picForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields =  ['profile_pic']

class storyForm(ModelForm):
	class Meta:
		model = Scribble
		fields = ['headline','story','scribble_type']	

class userinfo_Form(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['bio']
		
class ReportForm(ModelForm):
    class Meta:
        model=Report
        fields='__all__'
        exclude=['reported_by','on','scribble']

def mylogin(request):
	context = RequestContext(request,
                           {'request': request,
                            'user': request.user})

	
	if (request.user.is_authenticated()):# if user is already logged in and tries to login again
		print("biii")
		return redirect('home')	#make it goto home
	if(request.method == 'GET'):
		form = AuthenticationForm()
		
		signup=UserCreationForm()
		return render(request, 'login.html', {'form': form,'signupform':signup})
		
	else:
		form = AuthenticationForm(request,data = request.POST)
		print("hii")
		print(form)
		if form.is_valid():
			print("yuhooo")
			login(request, form.get_user())
			return redirect('home')
	#if form2.is_valid():
	#	new_user = form2.save()
	#	login(request, form2.get_user())
	#	return redirect('home')
			
		form = AuthenticationForm()
	return render(request, 'login.html',{'form':form})
def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        print("bii")
        form = UserCreationForm(request.POST)
        args['form'] = form
        print("kiii")
        if form.is_valid():
            print("wow")
            form.save()  # save user to database if form is valid
            print("hii")
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]   
            activation_key = hashlib.sha1((salt+email).encode('utf-8')).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user user username
            user=CustomUser.objects.get(username=username)

            # Create and save user profile                                                                                                                                  
            new_profile = UserProfile(user=user, activation_key=activation_key, 
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://127.0.0.1:8000/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'rkap95@gmail.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/register_success')
    else:
        args['form'] = UserCreationForm()

    return render_to_response('user_profile/register.html', args, context_instance=RequestContext(request))
		

def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('user_profile/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('user_profile/confirm.html')		

@login_required	
def register_success(request):
	data=Scribble.objects.all()
	print(data[1].user)
	
	form2=commentForm()
	user=request.user
	return render(request,'home.html',{"item_list":data ,'form2' : form2,'user':user})

#ef register(request):
#if request.method == 'POST':
#	form2 = signupForm(request.POST)
#	if form2.is_valid():
#		new_user = form2.save()
			
#		return render(request,'home.html',{'user':new_user})
#else:
#	form3 = signupForm()
#return render(request, "login.html", {
	#'form3': form3,
 #  })
		

		
class commentForm(ModelForm):
	class Meta:
		model=Comment
		fields = '__all__'
		exclude = ['comment_user','on','Scribble']
		
class signupForm(ModelForm):
	class Meta:
		model=CustomUser
		fields = '__all__'
		exclude = ['profile_pic','following']

colors=['#1ABC9C','#16A085','#2ECC71','#27AE60','#3498DB','#2980B9','#9B59B6','#8E44AD','#34495E','#2C3E50','#F1C40F','#F39C12','#E67E22','#D35400','#E74C3C','#C0392B']
		
@login_required	
def home(request):
	datagot=Scribble.objects.all().order_by('-on')
  #  print(data[1].user)
	print("hii")
	if request.is_ajax():
		print("hoo")
		obj_id=request.GET.get('feedobj')
		obj=Scribble.objects.get(id=obj_id)
		time=obj.on
		print(time)
		story=Scribble.objects.filter(on__lte=time).order_by('-on')[:10]
		user=request.user
		home=1
		if story.count() == 0 :
			return HttpResponse("<p>No more stories</p>", content_type="text/plain")
		else:	
			rendered= render_to_string('content.html',{"item_list":story,'user':user,'home':home,'colors':colors,'person':user})
			return HttpResponse(rendered)
    #comments=data.Comment_set.all()
    #print(comments)
	else:
		print("bii")
		user=request.user
		form=storyForm()
		form_comment=commentForm()
		reportform=ReportForm()
		home=1
    #obj=get_object_or_404(Comment,pk=1)
	#data=serializers.serialize("json",datagot,indent=8)
	#return HttpResponse(data,content_type='application/json')
    #HttpResponse(json.dumps(data), content_type = 'application/json')
		return render(request,'home.html',{"item_list":datagot[:4] ,'user':user,'colors':colors,'person':user,'home':home})



@login_required
def mylogout(request):
    logout(request)
    return redirect('/login')

	
	
@login_required
@require_http_methods(["GET"])
def autocomplete(request):
    print("kii")
    term = request.GET.get('term', '')
    print (term)
    if (term == ''):
        data = []
    else:
        print("hii")
        users = CustomUser.objects.filter(username__icontains = term)
        #Scribble=Scribble.objects.filter(hash_tags__icontains = term)
        data = [ {'label': user.get_full_name(), 'value' : user.id } for user in users ]
    return HttpResponse(json.dumps(data), content_type = 'application/json')        



		
@login_required
def profile(request):
	item = get_object_or_404(CustomUser, id=request.user.id)
	if(item.profile_pic):
		profilepic=item.profile_pic
		form=userinfo_Form()
		#relations=Relationship.objects.filter(from_person__id=request.user.id)
		#gut=CustomUser.objects.filter(related_to=request.user.id)
		userScribble=Scribble.objects.filter(user=request.user).order_by('-on')
		return render(request,'profile.html',{'person':item ,'profilepic':profilepic,'form':form,'item_list':userScribble,'colors':colors})
	else:
		userScribble=Scribble.objects.filter(user=request.user).order_by('-on')
		form=userinfo_Form()
		return render(request,'profile.html',{'form':form,'item_list':userScribble,'person':item,'profilepic':1,'colors':colors})
	
@login_required
def addprofilepic(request):
	if request.method == 'POST':
		
		#form=profile_picForm(request.POST,request.FILES)
		user=get_object_or_404(CustomUser, id=request.user.id)
		user.profile_pic=request.FILES.get('profile_pic')
		
		#print(form)
		
		
		
		#if form.is_valid():
		#	form.save();
			#return redirect('/thanku/')
		user.save()
	return redirect('/profile')

	
@login_required
def delprofilepic(request):
	#if request.method == 'POST'
		
		#form=profile_picForm(request.POST,request.FILES)
    user=get_object_or_404(CustomUser, id=request.user.id)
    user.profile_pic=""
		
		#print(form)
		
		
		
		#if form.is_valid():
		#	form.save();
			#return redirect('/thanku/')
    user.save()
    return redirect('/profile')



@login_required
def addinfo(request):
	if request.method == 'POST':
		form=userinfo_Form(request.POST)
		print("hii")
		print(form)
		if form.is_valid():
			print("bii")
			info=form.save(commit=False)
			info.user = CustomUser.objects.get(username=request.user.username)
			profile=UserInfo.objects.get(user=request.user)
			profile.bio=info.bio
			profile.save()	
			#info.save()
			return redirect('profile')
		else:
			return HttpResponse()
		
@login_required	
def show_user_id(request,user_id):
    try:
        user_id=int(user_id)
    except ValueError:
        raise Http404()
    item=get_object_or_404(CustomUser,pk=user_id)
    if(item.profile_pic):
        profilepic=item.profile_pic
        userScribble=Scribble.objects.filter(user=item)
        return render(request,'profile.html',{'person':item ,'profilepic':profilepic,'item_list':userScribble,'colors':colors})
    else:
        userScribble=Scribble.objects.filter(user=item)
        return render(request,'profile.html',{'item_list':userScribble,'person':item,'profilepic':1,'colors':colors})
	#data=serializers.serialize("json",[user],indent=8)
	#return HttpResponse(data,content_type='application/json')	

@login_required	
def add_relationship(request,user_id):
	item=get_object_or_404(CustomUser,pk=user_id)
	relationship, created = Relationship.objects.get_or_create(
        from_person=request.user,
        to_person=item,
        status=1)
	url='/users/' + user_id
	return redirect(url)

@login_required	
def remove_relationship(request,user_id):
	item=get_object_or_404(CustomUser,pk=user_id)
	obj=get_object_or_404(Relationship,
        from_person=request.user,
        to_person=item,
        status=1)
	obj.delete()
	url='/users/' + user_id
	return redirect(url)



def get_following(request):
	following=CustomUser.objects.filter(related_to=request.user.id)
	data=serializers.serialize("json",following,indent=8)
	return HttpResponse(json.dumps(data), content_type = 'application/json')        

def get_followers(request):
	followers=CustomUser.objects.filter(following=request.user.id)
	data=serializers.serialize("json",followers,indent=8)
	return HttpResponse(json.dumps(data), content_type = 'application/json')        

#	return HttpResponse(followers)