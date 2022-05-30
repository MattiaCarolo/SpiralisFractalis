from django.db import models
from django.db.models import fields
from rest_framework import serializers
from evalfract.models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = (
            "image",
            "score",
            "transformations",
        )
