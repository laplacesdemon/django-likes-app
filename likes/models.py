from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from likes.managers import LikeManager

class Like(models.Model):
    unique_together = (("user", "object_id", "content_type"),)
    
    objects = LikeManager()
    
    user = models.ForeignKey(User)
    when = models.DateTimeField(auto_now=True)
    
    content_type = models.ForeignKey(ContentType) # the type of the entity
    object_id = models.PositiveIntegerField() # the primary key of the entity
    content_object = generic.GenericForeignKey("content_type", "object_id") # content type and fk id
    
    def __unicode__(self):
        return "Like %s by %s" % (self.content_object, self.user)