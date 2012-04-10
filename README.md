===========
Zuqqa Likes
===========

A Django app to have Facebook or Google+ style likes.
You can attach "like" functionalty to any model you want and allow your users to like them.
Currently, only registered users can like an object

Disclaimer
----------

This app doesn't extend any other models in runtime (i.e. using add_to_class method).

Usage
-----

sample objects, don't forget to include model classes

    user = User.objects.get(username="sample_user")
    story = Story.objects.get(name="sample_story") 

create and save a like object
    
    like = Like(user=user, content_object=story)
    like.save()

get likes manually

    likes = Like.objects.for_model(story).order_by("-when")
    [<like1>,<like2>]

    likes_count = Like.objects.count_for_model(story)
    2

get the user's likes
    users_likes = Like.objects.for_user(user).order_by("-when")
    [<like1>,<like2>]

    count = Like.objects.count_for_user(user)
    2