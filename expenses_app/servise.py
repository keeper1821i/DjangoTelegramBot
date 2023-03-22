import itertools


def top_cat(queryset, k):
    cat_dict = {}
    for i in queryset.iterator():
        if i.category in cat_dict:
            cat_dict[i.category] += 1
        else:
            cat_dict[i.category] = 1
    sorted_tuples = sorted(cat_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = {k: v for k, v in sorted_tuples}
    print(sorted_dict)
    return dict(itertools.islice(sorted_dict.items(), int(k)))
