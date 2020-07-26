from django.conf import settings
from rest_framework import serializers

from .models import Tweet


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError('This is not a valid action for tweets')
        return value


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ['content']

    def validate_content(self, value):
        if len(value) > settings.MAX_TWEET_LENGTH:
            raise serializers.ValidationError('This tweet is too long')
        return value