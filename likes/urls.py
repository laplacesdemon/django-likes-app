from django.conf.urls.defaults import *

urlpatterns = patterns('likes.views',
    (r'^create/$', 'create'), # create like
    (r'^remove/$', 'remove'),
)
