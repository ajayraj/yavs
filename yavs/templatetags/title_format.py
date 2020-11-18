from django import template
from yavs.models import Video
import os

register = template.Library()

@register.simple_tag
def tb_path(video_path):
    file, extension = os.path.splitext(video_path)
    return file + "_tb.png"
