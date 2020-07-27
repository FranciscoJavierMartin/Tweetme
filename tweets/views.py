from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer


ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.POST)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def tweets_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    qs = qs.filter(user=request.user)
    if not qs.exitsts():
        return Response({'message': 'You cannot delete this tweet'},
                        status=status.HTTP_403_FORBIDDEN)

    obj = qs.first()
    obj.delete()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, tweet_id, *args, **kwargs):
    """
    id is required
    Action options are: like, unlike, retweet
    """
    serializer = TweetActionSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')

        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        obj = qs.first()

        if action == 'like':
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if action == 'unlike':
            obj.likes.remove(request.user)
        elif action == 'retweet':
            parent_obj = obj
            new_tweet = Tweet.objects.create(
                user=request.user, parent=parent_obj)

    return Response({}, status=status.HTTP_200_OK)

# def tweet_create_view_pure_django(request, *args, **kwargs):
#     """
#     REST API Create view
#     """
#     user = request.user

#     if not user.is_authenticated:
#         if request.is_ajax():
#             return JsonResponse({}, status=401)

#         return redirect(settings.LOGIN_URL)

#     form = TweetForm(request.POST or None)
#     next_url = request.POST.get('next') or None

#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = user
#         obj.save()

#         if request.is_ajax():
#             return JsonResponse(obj.serialize(), status=201)

#         if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
#             return redirect(next_url)

#         form = TweetForm()

#     if form.errors:
#         if request.is_ajax():
#             return JsonResponse(form.errors, status=400)

#     return render(request, 'components/form.html', context={'form': form})


# def tweets_list_view_pure_django(request, *args, **kwargs):
#     """
#     REST API View
#     Consume by JavaScript
#     return json data
#     """
#     qs = Tweet.objects.all()
#     tweets_list = [x.serialize() for x in qs]
#     data = {
#         'isUser': False,
#         'response': tweets_list
#     }
#     return JsonResponse(data)


# def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
#     """
#     REST API view
#     return json data
#     """
#     data = {
#         'id': tweet_id,
#     }

#     try:
#         obj = Tweet.objects.get(id=tweet_id)
#         data['content'] = obj.content
#     except:
#         data['message'] = 'Not found'
#         status = 404

#     return JsonResponse(data, status=status)
