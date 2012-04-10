from django.conf.urls.defaults import *

urlpatterns = patterns('zuqqa_likes.views',
	(r'^create/$', 'create'), # create like
)
