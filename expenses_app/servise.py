import itertools
from django.contrib.auth.models import User

from bot_app.models import Profile


def top_cat(queryset, k):
    cat_dict = {}
    cat_list = []
    for i in queryset.iterator():
        if i.category in cat_dict:
            cat_dict[i.category] += 1
        else:
            cat_dict[i.category] = 1
    sorted_tuples = sorted(cat_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = {k: v for k, v in sorted_tuples}
    for key, value in sorted_dict.items():
        cat_list.append({'category': key, 'quantity': value})
    return cat_list[:int(k)]


def check_token(token, user):
    queryset = Profile.objects.all()
    user = User.objects.get(username='User' + user)
    profile = queryset.get(user=user.id)
    if profile.token == token:
        return True
    else:
        return False
