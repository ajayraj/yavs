from django import template
import os

register = template.Library()

@register.simple_tag
def tb_path(video_path):
    file, extension = os.path.splitext(video_path)
    return file + "_tb.png"
