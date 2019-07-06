# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

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
    LINK_TYPE = (
        (0, _('Internal')),
        (1, _('External')),
    )
    name = models.CharField(max_length=255, verbose_name=_('name'))
    position = models.CharField(
        max_length=255, default='left', verbose_name=_('Menu Position'))
    link_type = models.IntegerField(default=0, choices=LINK_TYPE,
                                    verbose_name=_('Link Type'))
    link = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name=_('Link'))
    icon = models.CharField(max_length=255,
                            blank=True,
                            null=True,
                            verbose_name=_('Icon'))
    content_type = models.ForeignKey(ContentType, blank=True,
                                     verbose_name=_('ContentType'),
                                     on_delete=models.CASCADE)

    valid = models.BooleanField(default=True, verbose_name=_('Valid'))
    node_order_by = ['name', 'position']

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu Setting')
