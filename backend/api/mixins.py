class IsSubscribedMixin:
    """Checking if the user is subscribed."""

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return obj.subscribers.filter(user=user).exists()
        return False
