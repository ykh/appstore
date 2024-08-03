from apps.models import App, Purchase
from appstore.utils.permission import permission
from users.models import User


@permission
def has_create_permission(customer: User, app: App):
    if customer.id == app.user.id:
        return False

    if not app.is_verified or not app.is_activated:
        return False

    return customer.is_authenticated

