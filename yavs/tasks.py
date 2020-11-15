from django_rq import job
from .models import Video
from django.conf import settings
import os, sys, logging
import speech_recognition as sr

logger = logging.getLogger(__name__)

def video_to_audio(file_path):
    try:
        file, extension = os.path.splitext(file_path)
        os.system('ffmpeg -i {file}{ext} {file}.wav'.format(file=file, ext=extension))
        print('"{}" converted to WAV'.format(file_path))
        return "{}.wav".format(file)

    except OSError as err:
        print(err.reason)
        exit(1)

def chunked_audio_to_text(file_path):
    r = sr.Recognizer()
    
    audio_file = sr.AudioFile(file_path)
    transcribed_text = ""
    consecutive_error = 0
    
    with audio_file as source:
        while(True):
            print("New chunk creation attempted")
            audio = r.record(source, duration=30)
            
            try:
                chunk_transcribed = r.recognize_google(audio)
                transcribed_text += " " + chunk_transcribed
                consecutive_error = 0
                
            except sr.UnknownValueError:
                print("Could not understand audio.")
                consecutive_error += 1
                if (consecutive_error >= 3):
                    break
                    
            except sr.RequestError as e:
                print("Could not request results.")
                break

    return transcribed_text

def video_to_text(file_path):
    response = chunked_audio_to_text(video_to_audio(file_path))
    if not response:
        return (False, response)
    else:
        return (True, response)

@job
def generate_insights_for_video(video_id):
    logger.info("Generating Insights") 
    
    # Steps:

    # Grab audio from video

    # Upload audio to api to transcribe to text

    # Use text for NLP analyses, fill out sentiment field, generate visualization pics for new "insights" view, etc.
    print("GENERATE INSIGHT FUNCTION CALLED")
    #video = Video.objects.get(id=video_id)
    #video.sentiment = "test"
    #video.save()
    #media_dir = settings.MEDIA_URL
    video = Video.objects.get(id=video_id)
    curr_path = os.getcwd()
    Video.objects.filter(id=video_id).update(sentiment=curr_path)
    os.chdir("/home/sum/projects/yavs/media")
    response = video_to_text(str(video.path))
    if (response[0]):
        Video.objects.filter(id=video_id).update(sentiment="INSIGHT_ABLE_TO_GENERATE")
    else:
        Video.objects.filter(id=video_id).update(sentiment="INSIGHT_NOT_ABLE_TO_GENERATE")

    os.chdir("/home/sum/projects/yavs")
