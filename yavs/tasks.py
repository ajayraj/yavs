from django_rq import job
from .models import Video
from django.conf import settings
from os import path
import os, sys, logging
import spacy
import speech_recognition as sr
from wordcloud import WordCloud
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def video_to_audio(file_path, video_id):
    file, extension = os.path.splitext(file_path)
    os.system('ffmpeg -i {file}{ext} {file}.wav'.format(file=file, ext=extension))
    print('"{}" converted to WAV'.format(file_path))

    audio_path = "{}.wav".format(file)

    if path.exists(audio_path):
        return audio_path
    else:
        Video.objects.filter(id=video_id).update(sentiment="NO_AUDIO")
        sys.exit()


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

def video_to_text(file_path, video_id):
    response = chunked_audio_to_text(video_to_audio(file_path, video_id))
    if not response:
        return (False, response)
    else:
        return (True, response)

def text_analysis(transcribed_content):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(transcribed_content)
    # Removing stopwords
    token_list = [token for token in doc if not token.is_stop]
    # Can lemmatize
    lemma_list = [token.lemma_ for token in token_list]
    
    text = " ".join(map(str, lemma_list))
    return text

def plot_wordcloud(cleaned_string):
    wordcloud = WordCloud(width = 800, height = 800, 
                          background_color ='white',
                          stopwords=[],
                          min_font_size = 10).generate(cleaned_string) 

    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.show()
    return wordcloud

def video_to_wordcloud(file_path):
    text_content = video_to_text(file_path)
    if (text_content[0]):
        cleaned_text = text_analysis(text_content[1])
        wc = plot_wordcloud(cleaned_text)
        file, extension = os.path.splitext(file_path)
        wc.to_file("{}.png".format(file))

@job
def generate_insights_for_video(video_id):
    logger.info("Generating Insights") 
    
    print("GENERATE INSIGHT FUNCTION CALLED")

    # Get video and update sentiment field to current working directory, useful for debug
    video = Video.objects.get(id=video_id)
    curr_path = os.getcwd()
    Video.objects.filter(id=video_id).update(sentiment=curr_path)
    os.chdir("/home/sum/projects/yavs/media")
    
    response = video_to_text(str(video.path), video_id)

    if (response[0]):
        Video.objects.filter(id=video_id).update(sentiment="INSIGHT_ABLE_TO_GENERATE")
        cleaned_text = text_analysis(response[1])
        wc = plot_wordcloud(cleaned_text)
        file, extension = os.path.splitext(video.path)
        wc.to_file("{}.png".format(file))
        
    else:
        Video.objects.filter(id=video_id).update(sentiment="INSIGHT_NOT_ABLE_TO_GENERATE")

    os.chdir("/home/sum/projects/yavs")
