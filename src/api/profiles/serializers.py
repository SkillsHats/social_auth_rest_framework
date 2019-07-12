from rest_framework import serializers

from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    email   = serializers.CharField(source='user.email')
    bio     = serializers.CharField(allow_blank=True, required=False)
    image   = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('email', 'bio', 'image',)
        read_only_fields = ('email',)

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
