from rest_framework import serializers
from art_pieces.models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id', 'title', 'artist', 'medium', 'published')
