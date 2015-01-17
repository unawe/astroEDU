import django.shortcuts

from astroedu.django_ext.models import ArchivalModel


def _get_queryset(klass, user, order_by=None, select_related=None):
    if issubclass(klass, ArchivalModel) and user and user.is_authenticated():
        queryset = klass._default_manager.all(user=user)
    else:
        queryset = django.shortcuts._get_queryset(klass)
    if select_related:
        queryset = queryset.select_related(*select_related)
    if order_by:
        queryset = queryset.order_by(order_by)
    return queryset


def get_object_or_404(klass, user=None, select_related=None, *args, **kwargs):
    queryset = _get_queryset(klass, user, select_related=select_related)
    return django.shortcuts.get_object_or_404(queryset, *args, **kwargs)


def get_list_or_404(klass, user=None, order_by=None, select_related=None, *args, **kwargs):
    queryset = _get_queryset(klass, user, order_by=order_by, select_related=select_related)
    return django.shortcuts.get_list_or_404(queryset, *args, **kwargs)
