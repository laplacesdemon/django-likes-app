from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from likes.models import Like
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

@login_required
@require_http_methods(["POST"])
def create(request):
    """
    create the like object
    """
    content_type_pk = request.POST.get("ct")
    object_id = request.POST.get("id")
    
    # create the object
    like = Like.objects.create_like(request.user, content_type_pk, object_id)
    
    if(request.is_ajax()):
        callback    = {"cmd": "callback", "e": "likes_added", "parameter": "id=%s" % like.id}
        callback2   = {"cmd": "callback", "e": "likes_increase_counter",  "parameter": object_id}
        data        = [callback, callback2]
        json        = simplejson.dumps(data)
        return HttpResponse(json, mimetype='application/json')
    else:
        from django.contrib import messages
        messages.add_message(request, messages.INFO, 'Operation is successful.')
        return HttpResponseRedirect("/")

@login_required
@require_http_methods(["POST"])
def remove(request):
    """
    removes the like from the object
    """
    like_id = request.POST.get("id")
    
    # remove it 
    like = Like.objects.get(pk=like_id)
    ct = like.content_type.id
    o_id = like.object_id
    like.delete()
    
    if(request.is_ajax()):
        callback    = {"cmd": "callback", "e": "likes_removed",  "parameter": "ct=%s&id=%s" % (ct, o_id)}
        callback2   = {"cmd": "callback", "e": "likes_decrease_counter",  "parameter": o_id}
        data        = [callback, callback2]
        json        = simplejson.dumps(data)
        return HttpResponse(json, mimetype='application/json')
    else:
        from django.contrib import messages
        messages.add_message(request, messages.INFO, 'Operation is successful.')
        return HttpResponseRedirect("/")