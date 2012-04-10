from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

class LikeManager(models.Manager):
    
    def for_model(self, model):
        """
        return all the likes of the given object
        """
        content_type = ContentType.objects.get_for_model(model)
        query_set = self.get_query_set().filter(content_type=content_type)
        if isinstance(model, models.Model):
            query_set = query_set.filter(object_id=force_unicode(model._get_pk_val()))
        return query_set
    
    def for_user(self, user):
        """
        return given user's likes
        """
        return self.get_query_set().filter(user=user)
        
    def count_for_model(self, model):
        """
        return the total # of counts for given model
        """
        content_type = ContentType.objects.get_for_model(model)
        query_set = self.get_query_set().filter(content_type=content_type)
        if isinstance(model, models.Model):
            query_set = query_set.filter(object_id=force_unicode(model._get_pk_val()))
        return query_set.count()
        
    def count_for_user(self, user):
        """
        return given user's likes
        """
        return self.get_query_set().filter(user=user).count()
        
    def create_like(self, user, content_type_pk, object_id):
        """
        creates the like object
        useful method to create the like object without having the model instance
        content_type_pk is the primary key of the content type
        """
        from zuqqa_likes.models import Like
        ct = ContentType.objects.get(pk=content_type_pk)
        content_object = ct.get_object_for_this_type(id=object_id)
        like = Like(user=user, content_object=content_object)
        like.save()
        return like
    
    def remove_like(self, like_id):
        """
        removes the like of the given id
        """
        from zuqqa_likes.models import Like
        like = Like.objects.get(pk=like_id)
        like.delete()