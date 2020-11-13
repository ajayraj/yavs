from django_rq import job
from .models import Video
import logging
logger = logging.getLogger(__name__)

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
    Video.objects.filter(id=video_id).update(sentiment="test")
