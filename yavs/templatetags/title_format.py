from django import template
from .models import Video
import os

register = template.Library()

@register.simple_tag
def tb_path(video_path):
    file, extension = os.path.splitext(video_path)
    return file + "_tb.png"

@register.simple_tag
def which_category(response):
    return response.partition("|")[2] 

@register.simple_tag
def has_insights(response):
    if response is None:
        return False
    else:
        return "|" in response
