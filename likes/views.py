from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from zuqqa_likes.models import Like
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect

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
        callback    = {"cmd": "callback", "e": "likes_added", "parameter": ""}
        data        = [callback]
        json        = simplejson.dumps(data)
        return HttpResponse(json, mimetype='application/json')
    else:
        from django.contrib import messages
        messages.add_message(request, messages.INFO, 'Operation is successful.')
        return HttpResponseRedirect("/")
