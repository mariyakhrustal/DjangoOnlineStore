from django import template

register = template.Library()


@register.filter()
def blogs_media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"
