from django.shortcuts import render
from django.views.generic.base import View, HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .forms import SignInForm, SignUpForm, UploadVideoForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Video, Comment
from pathlib import Path
from django.conf import settings
import string, random, os
#For development
from wsgiref.util import FileWrapper

# For Test:
#   Use workaround to make files downloadable via get request through filegrab view
#   Request from own public endpoint?
#   Convert to proper media model and hosted static server when deploying

# TO FIX FOR PROD:
#   Serve static/media files from NGINX server
#   Media: user uploaded
#       https://overiq.com/django-1-10/handling-media-files-in-django/
#       https://docs.djangoproject.com/en/3.1/howto/static-files/deployment/
#   Asynchronous tasks: sentiment analysis + visualizations (use Celery?)
#       https://overiq.com/django-1-11/asynchronous-tasks-with-celery/
#   DATABASE: Switch from sqlite3 to postgresql

class Home(View):
    template_name = "index.html"
    def get(self, request):

        most_recent = Video.objects.order_by('-born_on')[:10] # grab 10 most recent videos

        return render(request, self.template_name, {'most_recent': most_recent})

class UploadVideo(View):
    template_name = "upload_video.html"

    def get(self, request):
        if request.user.is_authenticated == False:
            print("User not logged in, redirecting.")
            return HttpResponseRedirect('sign_up')
        form = UploadVideoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UploadVideoForm(request.POST, request.FILES)
        print(form)
        print(request.POST)
        print(request.FILES)
        if form.is_valid():
            # Create a Video
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            upload_vid = form.cleaned_data['file']

            prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            path = prefix + upload_vid.name

            
            fs = FileSystemStorage(location = settings.MEDIA_ROOT)
            filename = fs.save(path, upload_vid)
            file_url = fs.url(filename)

            print("FILESYSTEM",fs)
            print("FILENAME",filename)
            print("FILE_URL",file_url)

            new_video = Video(title=title, description=description, uploaded_by=request.user, path=path)
            print("CURRENT DIRECTORY FOR VID UPLOAD:", Path.cwd())
            new_video.save()

            # redirects to video page
            return HttpResponseRedirect("/video_player/{}".format(new_video.id))

        else:
            print(form)
            print(request.FILES)
            return HttpResponse("Invalid Upload Form")

class SignIn(View):
    template_name = "sign_in.html"
    
    def get(self, request):
        if request.user.is_authenticated:
            print("User already logged in, redirecting.")
            print(request.user)
            return HttpResponseRedirect('/')

        form = SignInForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        print("SignIn POST Called")
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # create new entry in table logs?
                login(request, user) #persists login session
                print("Successful login")
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('login')

        print(request)
        return HttpResponse("This is the SignIn View POST Request")

class SignUp(View):
    template_name = "sign_up.html"
    
    def get(self, request):
        if request.user.is_authenticated:
            print("User already logged in, redirecting.")
            print(request.user)
            return HttpResponseRedirect('/')

        form = SignUpForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        print("SignUp POST Called")
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create An Account
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            #check_email = User.objects.get(email=email)
            
            #if check_email is not None:
            #   return "Email is taken"
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return HttpResponseRedirect("/sign_in")
        print(request)
        return HttpResponse("This is the SignUp View POST Request")

# File Media Server for development
class VideoGrab(View):
    def get(self, request, file_name):
        BASE_DIR = Path(__file__).resolve().parent.parent
        video_to_serve = FileWrapper(open(str(BASE_DIR) + '/' + file_name, 'rb'))
        response = HttpResponse(video_to_serve, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response


class VideoPlayer(View):
    template_name = "video_player.html"

    def get(self, request, id):
        # most_recent = Video.objects.order_by('-born_on')[:10] # grab 10 most recent videos
        # Grab information for video by ID
        media_dir = settings.MEDIA_URL
        video_to_serve = Video.objects.get(id=id)
        #BASE_DIR = Path(__file__).resolve().parent.parent
        #video_to_serve.path = "http://yavs.ajayraj.co/get_video/" + video_to_serve.path
        video_to_serve.path = media_dir + video_to_serve.path
        
        print("PATH THAT WILL BE PASSED TO VIDEO VIEW: ", video_to_serve.path)
        print("CURRENT WORKING DIRECTORY: ", os.getcwd())

        context = {'video':video_to_serve}
        context['comments'] = Comment.objects.filter(video=video_to_serve)

        # Cannot submit comment unless logged in as a user
        print("CHECKING IF USER IS AUTHENTICATED")
        if request.user.is_authenticated:
            print("USER IS AUTHENTICATED")
            comment_form = CommentForm()
            context['form'] = comment_form
            print("FORM IS CREATED")

        # Fix DoesNotExist range exception try catch

        return render(request, self.template_name, context)


class PostComment(View):
    template_name = "comment.html"
    
    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            #video = form.cleaned_data['video']
            video_id = request.POST['video']
            video = Video.objects.get(id=video_id)

            comment_to_submit = Comment(text=comment, user=request.user, video=video)
            comment_to_submit.save()
            return HttpResponseRedirect('/video_player/{}'.format(str(video_id)))

class SignOut(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

class UserProfile(View):
    template_name = "user_profile.html"
    def get(self, request, user_requested):
        target = User.objects.get(username=user_requested)

        user_uploaded = Video.objects.filter(uploaded_by=target.id).order_by('-born_on')

        return render(request, self.template_name, {'target' : user_requested, 'user_uploaded': user_uploaded})
