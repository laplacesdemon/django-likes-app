from django import template

register = template.Library()
    
@register.inclusion_tag('likes/inclusion_tags/print_links.html', takes_context=True)
def print_like_link(context, obj):
    """
    prints the link using the inclusion template
    """
    request = context["request"]
    from likes.models import Like
    try:
        like = Like.objects.for_model(obj).filter(user=request.user).all()[0]
    except:
        like = None
        
    context.update({
        'obj': obj,
        'like': like,
    })
    return context