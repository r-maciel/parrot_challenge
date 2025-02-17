from api.models.user import User


class Waiter(User):
    """ Proxy model for waiters """

    class Meta:
        """ Meta class for Waiter proxy model """
        proxy = True

    def save(self, *args, **kwargs):
        """ Set is_staff for all waiters """
        self.is_staff = True
        super().save(*args, **kwargs)
