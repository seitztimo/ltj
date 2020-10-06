from django.contrib.auth import get_user_model


def make_user(username="testuser", is_admin=True):
    user_model = get_user_model()
    return user_model.objects.create(
        username=username, is_staff=is_admin, is_superuser=is_admin
    )
