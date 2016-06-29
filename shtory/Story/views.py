from django.shortcuts import render
from django.forms import ModelForm , RadioSelect
from Story.models import *
from django.shortcuts import render, get_object_or_404, redirect
from Myuser.models import *
from django.http import HttpResponseRedirect ,HttpResponse
from django.contrib.auth.decorators import login_required
import re
from django import forms
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from django.utils import timezone
from django.core import serializers
from django.conf import settings
# Create your views here.


class storyForm(ModelForm):
	class Meta:
		model = Scribble
		fields = ['headline','story','scribble_type']
		     

class commentForm(ModelForm):
	class Meta:
		model=Comment
		fields =['text']
        
class ReportForm(ModelForm):
    class Meta:
        model=Report
        fields='__all__'
        exclude=['reported_by','on','scribble']


def addstory(request):
	if request.method == 'POST':
		form = storyForm(request.POST)
		if form.is_valid():
			story=form.save(commit=False)
			story.user = CustomUser.objects.get(username=request.user)
			#print(story.is_poem)
			#story.save()
			#print(story.id)
			pat=re.compile(r"#(\w+)")
			tag=pat.findall(story.headline)
			#print(tag[0])
			#print(tag[1])
			for index in range(len(tag)):
				found=HashTag.objects.filter(name = tag[index])
				print(found)
				if not found:
					myhash=HashTag(name=tag[index])
					myhash.count+=1
					myhash.save()
				#	hashlen=hash.count + ''
					print(myhash.name)
					link='<a class="hash" href="/searchquery/?q='+ myhash.name + '">' + myhash.name + '<small>('+ str(myhash.count) + ')</small></a>'
					print(link)
					print("oye")
					story.headline=story.headline.replace(myhash.name,link)
					story.save()
					print(story)
					story_added=get_object_or_404(Scribble,pk=story.id)
					story_added.hash_tags.add(myhash)
			#		return redirect('/userstory/')
				else:
					story.save()
					#story_added=get_object_or_404(Scribble,pk=story.id)
					myhash=HashTag.objects.get(name=tag[index])
					link='<a  class="hash" href="/searchquery/?q='+ myhash.name + '">' + myhash.name + '<small>('+ str(myhash.count) + ')</small></a>'
					print("toye")
					story.headline=story.headline.replace(myhash.name,link)
					story.save()
					story.hash_tags.add(HashTag.objects.get(name = tag[index]))
					foundtag=HashTag.objects.get(name = tag[index])
					foundtag.count=foundtag.count+1
			#		return redirect('/userstory/')
			story.save()	
			return redirect('/userstory/')
	return redirect('/login/')
	    #  <a href="#" class="btn btn-primary" role="button"><b>FPS</b> <small>(12)</small></a>


colors=['#1ABC9C','#16A085','#2ECC71','#27AE60','#3498DB','#2980B9','#9B59B6','#8E44AD','#34495E','#2C3E50','#F1C40F','#F39C12','#E67E22','#D35400','#E74C3C','#C0392B']

def userstory(request):
	userstory=Scribble.objects.filter(user=request.user).order_by('-on')
	userstorypage=1
	return render(request,'home.html',{'item_list' : userstory,'userstorypage':userstorypage,'colors':colors})
	

def followerstory(request):
	user=CustomUser.objects.filter( id=request.user.id)
	print(Relationship.objects.filter(from_person__id=request.user.id))
	relations=Relationship.objects.filter(from_person__id=request.user.id)
	gut=CustomUser.objects.filter(related_to=request.user.id)
	folstory=[]
	print(gut)
	for i in range (gut.count()) :
		
		folstory.insert(i,Scribble.objects.filter(user=gut[i].id))

	#userrecipe=Recipe.objects.filter(by=request.user)
	#data=sorted(folstory,key=lambda instance: instance.date,reverse=True)
	#data=sorted(folstory,key=lambda instance: instance.time,reverse=True)
	print(folstory)
	user=request.user
	import itertools
	merged = list(itertools.chain(*folstory))
	return render(request,'home.html',{"item_list":merged,'user':user,'colors':colors,'person':user})         

@login_required	
@require_http_methods(["POST"])
def addcomment(request):
    print("booo")
    if request.method == 'POST':
        if(request.POST.get('text')):
            print("hooo")
            story1=get_object_or_404(Scribble,pk=request.POST.get('story'))
            user=CustomUser.objects.get(username=request.user.username)
            texty=request.POST.get('text')
            storyId=story1.id
            comment=Comment(comment_by=user,scribble=story1,text=texty)
            comment.save()
            return HttpResponse(comment.id)
        else:
            return HttpResponse('<p>Please enter some text</p>')
        
    else:
        return HttpResponse('<p>Page not found</p>')



@login_required
def vote_story(request):
    story=get_object_or_404(Scribble,pk=request.POST.get('story'))
    story.points+=1
    story.save()
    print("hii")
    user=request.user
    user.scribbles_liked.add(story)
    user.save()
    result=story.points
    return HttpResponse(result) 


@login_required
def bookmark(request):
    user=request.user
    bookedstory=user.scribbles_bookmarked.all()
    #pinnedrecipe=user.recipe_pinned.all()
    booked=sorted(
    bookedstory,
    key=lambda instance: instance.on)
    return render(request,'home.html',{"item_list":booked,'user':user, 'colors':colors})
    
@login_required
@require_http_methods(["POST"])
def edit_story(request):
	scribble=get_object_or_404(Scribble,pk=request.POST.get('story'))
	if story.user==request.user:
		text=request.POST.get('story_text')
		scribble.story=text
		scribble.save()
		return HttpResponse("edit done")

@login_required
@require_http_methods(["POST"])
def edit_comment(request):
	comment=get_object_or_404(Comment,pk=request.POST.get('comment_id'))
	if comment.comment_by==request.user:
		edit_text=request.POST.get('comment_text')
		comment.text=edit_text
		comment.save()
		return HttpResponse("comment edited ")

@login_required
@require_http_methods(["GET"])
def tagsearch(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		story_list = Scribble.objects.filter(hash_tags__name = q).order_by("-on")[:20]
		if (story_list):
			user=request.user
			return render(request, 'home.html',{"item_list":story_list,"user":user,"person":user,'colors':colors})
		elif not story_list:
			usersearch=get_object_or_404(CustomUser,username=q)
			if(usersearch):
				profilepic=usersearch.profile_pic
				userstory=Scribble.objects.filter(user=usersearch)
				return render(request,'profile.html',{'person':usersearch ,'profilepic':usersearch.profile_pic,'item_list':userstory,'colors':colors})
		else:
			return HttpResponse("<p>You are looking for something which dosen't exist</p>")
	else:
		return HttpResponse('Please submit a search term.')


@login_required
def delete_story(request):
    story=get_object_or_404(Scribble,pk=request.POST.get('story'))
    if story.user==request.user:
        story.delete()
        return HttpResponse()
    return HttpResponse(" you cannot delete stories posted by other users.")

@login_required
def delete_comment(request):
    comment=get_object_or_404(Comment,pk=request.POST.get('comment'))
    if comment.comment_by==request.user:
        comment.delete()
        return HttpResponse(" comment deleted")
    return HttpResponse(" you cannot delete comment posted by other users.")





@login_required
@require_http_methods(["POST"])
def reportstory(request):
	print(request.POST)
	story=get_object_or_404(Scribble,pk=request.POST.get('story_id'))
	user=request.user
    #user.photos_reported.add(photo)
    #user.save()
	reportform=ReportForm(request.POST)
	print(reportform)
	if reportform.is_valid():
		print("jii")
		report=reportform.save(commit=False)
		rep=Report(reason=report.reason,reported_by=user,scribble=story)
		user.stories_reported.add(story)
		rep.save()
		print("lii")
        #report.save()
		print("hogya")
		return redirect('/home/')
	else:
		return HttpResponse("<p>something went wrong your action couldn't be completed</p>")
     

	
@login_required
@require_http_methods(["POST"])
def book_story(request):
    story=get_object_or_404(Scribble,pk=request.POST.get('story'))
    story.book_points+=1
    story.save()
    print("hii")
    user=request.user
    user.scribbles_bookmarked.add(story)
    user.save()
    result=story.book_points
    print("hogya")
    return HttpResponse(result) 

