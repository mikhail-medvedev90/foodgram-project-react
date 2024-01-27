class IsSubscribedMixin:
    """Check if the given user is subscribed to the given object."""

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return obj.subscribers.filter(user=user).exists()
        return False
