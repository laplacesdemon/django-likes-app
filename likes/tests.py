from django.test import TestCase
from django.contrib.auth.models import User
from likes.models import Like
from django.test.client import Client
from django.contrib.contenttypes.models import ContentType

class ModelTest(TestCase):
    
    def _add_sample_likes(self, liker, liked):
        like = Like(user=liker, content_object=liked)
        like.save()
    
    def test_add_like(self):
        liker = User.objects.create_user("sample_user", "sample@user.com", "1234")
        popular = User.objects.create_user("popular_user", "popular@user.com", "1234")
        
        # test adding the like
        like = Like()
        like.user = liker
        like.content_object = popular
        like.save()
        self.assertEqual(like.content_object, popular)
        
    def test_fetch_likes(self):
        liker = User.objects.create_user("sample_user", "sample@user.com", "1234")
        popular = User.objects.create_user("popular_user", "popular@user.com", "1234")
        self._add_sample_likes(liker, popular)
        
        # test fetching of the likes of the popular user
        content_type = ContentType.objects.get_for_model(popular)
        likes = Like.objects.get(content_type__pk=content_type.id, object_id=popular.id)
        self.assertEqual(likes.content_object.id, popular.id)
        self.assertEqual(likes.user.id, liker.id)
        
    def test_cannot_like_more_than_once(self):
        self.fail("Disable liking more than once is NOT implemented yet")
        
    def test_fetch_likes_many(self):
        liker = User.objects.create_user("sample_user", "sample@user.com", "1234")
        liker2 = User.objects.create_user("sample_user2", "sample2@user.com", "1234")
        popular = User.objects.create_user("popular_user", "popular@user.com", "1234")
        self._add_sample_likes(liker, popular)
        self._add_sample_likes(liker2, popular)
        
        # test fetching of the likes of the popular user
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(popular)
        likes = Like.objects.filter(content_type__pk=content_type.id, object_id=popular.id).order_by("-when")
        self.assertEqual(2, likes.count())
        self.assertEqual(likes[0].content_object.id, popular.id)
        self.assertEqual(likes[0].user.id, liker.id)
        self.assertEqual(likes[1].content_object.id, popular.id)
        self.assertEqual(likes[1].user.id, liker2.id)
        
class ManagerTest(TestCase):
    
    def _add_sample_likes(self, liker, liked):
        like = Like(user=liker, content_object=liked)
        like.save()
    
    def test_create_like(self):
        liker = User.objects.create_user("sample_user", "sample@user.com", "1234")
        object_that_is_liked = User.objects.create_user("popular_user", "popular@user.com", "1234")
        
        ct = ContentType.objects.get_for_model(object_that_is_liked)
        like = Like.objects.create_like(liker, ct.id, object_that_is_liked.id)
        self.assertEqual(like.content_object, object_that_is_liked)
        self.assertEqual(like.user, liker)
        
    def test_remove_like(self):
        liker = User.objects.create_user("sample_user", "sample@user.com", "1234")
        object_that_is_liked = User.objects.create_user("popular_user", "popular@user.com", "1234")
        
        ct = ContentType.objects.get_for_model(object_that_is_liked)
        like = Like.objects.create_like(liker, ct.id, object_that_is_liked.id)
        self.assertEqual(like.content_object, object_that_is_liked)
        
        Like.objects.remove_like(like.id)
        self.assertEqual(like.content_object, object_that_is_liked)
        
        lik = Like.objects.for_model(object_that_is_liked)
        self.assertEqual(0, lik.count())
        
    def test_remove_unknown_like(self):
        pass
        #Like.objects.remove_like(666)
        #from django.core.exceptions import DoesNotExist
        #self.assertRaises(DoesNotExist, Like.objects.remove_like(666))
        
    def test_fetch_model_method_get_likes(self):
        liker = User.objects.create_user("sample_user", "sample@user.com", "1234")
        liker2 = User.objects.create_user("sample_user2", "sample2@user.com", "1234")
        popular = User.objects.create_user("popular_user", "popular@user.com", "1234")
        self._add_sample_likes(liker, popular)
        self._add_sample_likes(liker2, popular)
        
        # fetch the popular user's likes
        likes = Like.objects.for_model(popular).order_by("-when")
        self.assertEqual(2, likes.count())
        self.assertEqual(likes[0].content_object.id, popular.id)
        self.assertEqual(likes[0].user.id, liker.id)
        self.assertEqual(likes[1].content_object.id, popular.id)
        self.assertEqual(likes[1].user.id, liker2.id)
        self.assertEqual(2, Like.objects.count_for_model(popular))
        
    def test_get_users_likes(self):
        liker = User.objects.create_user("sample_user", "sample@user.com", "1234")
        liker2 = User.objects.create_user("sample_user2", "sample2@user.com", "1234")
        popular = User.objects.create_user("popular_user", "popular@user.com", "1234")
        self._add_sample_likes(liker, popular)
        self._add_sample_likes(liker, liker2)
        
        likes = Like.objects.for_user(liker).order_by("-when")
        self.assertEqual(2, likes.count())
        self.assertEqual(likes[0].content_object.id, popular.id)
        self.assertEqual(likes[1].content_object.id, liker2.id)
        self.assertEqual(2, Like.objects.count_for_user(liker))
        
class ViewTest(TestCase):
    
    fixtures = ['auth.json', 'likes.json']
    
    def test_create_like(self):
        user = User.objects.get(username="sample_user")
        popular = User.objects.create_user("create_like", "create@gmail.com", "1234")
        ct = ContentType.objects.get_for_model(popular)
        
        c = Client()
        c.login(username="sample_user", password="1234")
        response = c.post("/likes/create/", {
            'ct':ct.id, "id":popular.id,  
        })
        self.assertEqual(302, response.status_code)
        #self.assertEqual("OK", response.content)
        
        # make sure that the like object has been saved
        likes = Like.objects.for_model(popular).all()
        self.assertEqual(1, likes.count())
        self.assertEqual(popular.id, likes[0].content_object.id)
        self.assertEqual(ct.id, likes[0].content_type.id)
        self.assertEqual(user.id, likes[0].user.id)
        
    
    def test_create_like_ajax(self):
        user = User.objects.get(username="sample_user")
        popular = User.objects.create_user("create_like", "create@gmail.com", "1234")
        ct = ContentType.objects.get_for_model(popular)
        
        c = Client()
        c.login(username="sample_user", password="1234")
        response = c.post("/likes/create/", {
            'ct':ct.id, "id":popular.id,  
        }, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(200, response.status_code)
        #self.assertEqual("OK", response.content)
        
        # make sure that the like object has been saved
        likes = Like.objects.for_model(popular).all()
        self.assertEqual(1, likes.count())
        self.assertEqual(popular.id, likes[0].content_object.id)
        self.assertEqual(ct.id, likes[0].content_type.id)
        self.assertEqual(user.id, likes[0].user.id)
        
    def test_remove_like(self):
        user = User.objects.get(username="sample_user")
        popular = User.objects.create_user("create_like", "create@gmail.com", "1234")
        ct = ContentType.objects.get_for_model(popular)
        like = Like.objects.create_like(user, ct.id, popular.id)
        
        c = Client()
        c.login(username="sample_user", password="1234")
        response = c.post("/likes/remove/", {
            'ct':ct.id, "id":popular.id,  
        })
        self.assertEqual(302, response.status_code)
        #self.assertEqual("OK", response.content)
        
        # make sure that the like object has been saved
        is_deleted = False
        try:
            Like.objects.get(pk=like.id)
        except:
            is_deleted = True
        self.assertTrue(is_deleted)