# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission, Group

from treebeard.mp_tree import MP_Node


class Options(models.Model):
    option_name = models.CharField(
        max_length=255, unique=True, verbose_name=_('Option Name'))
    option_value = models.TextField(
        verbose_name=_('Option Value'))
    valid = models.BooleanField(default=True, verbose_name=_('Valid'))
    create_time = models.DateTimeField(
        default=timezone.now, verbose_name=_('CreateTime'))
    update_time = models.DateTimeField(
        auto_now=True, verbose_name=_('UpdateTime'))

    def __str__(self):
        return '{}'.format(self.option_name)

    class Meta:
        verbose_name = _('Options')
        verbose_name_plural = _('All Options')


class Menu(MP_Node):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    position = models.CharField(
        max_length=255, default='left', verbose_name=_('Menu Position'))
    link = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name=_('Link'))
    icon = models.CharField(max_length=255,
                            blank=True,
                            null=True,
                            verbose_name=_('Icon'))
    permission = models.ManyToManyField(Permission, blank=True,
                                        verbose_name=_('Permission'))

    permission_group = models.ManyToManyField(Group, blank=True,
                                              verbose_name=_(
                                                  'Permission Group'))

    valid = models.BooleanField(default=True, verbose_name=_('Valid'))
    node_order_by = ['name', 'position']

    def __str__(self):
        return '{}'.format(self.name)
