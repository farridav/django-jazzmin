# -*- coding: utf-8 -*-
import itertools
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from treebeard.mp_tree import MP_Node,\
    InvalidMoveToDescendant, MP_MoveHandler


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
        (3, _('Divide'))
    )
    name = models.CharField(max_length=255, verbose_name=_('name'))
    position = models.CharField(
        max_length=255, default='left', verbose_name=_('Menu Position'))
    link_type = models.IntegerField(default=0, choices=LINK_TYPE,
                                    verbose_name=_('Link Type'))
    link = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name=_('Link'),
                            help_text=_(
                                'support admin:index or /admin/ or http://'))
    icon = models.CharField(max_length=255,
                            blank=True,
                            null=True,
                            verbose_name=_('Icon'))
    content_type = models.ForeignKey(ContentType,
                                     blank=True, null=True,
                                     verbose_name=_('ContentType'),
                                     on_delete=models.CASCADE,
                                     help_text=_(
                                         'use for permission control.'))
    priority_level = models.IntegerField(default=100,
                                         verbose_name=_('Priority Level'),
                                         help_text=_('The bigger the priority'))
    valid = models.BooleanField(default=True, verbose_name=_('Valid'))
    node_order_by = ['priority_level']

    def move(self, target, pos=None):
        """
        Moves the current node and all it's descendants to a new position
        relative to another node.

        :raise PathOverflow: when the library can't make room for the
           node's new position
        """
        if target.depth == 2:
            raise InvalidMoveToDescendant(_('max depth is 2.'))
        return MP_MoveHandler(self, target, pos).process()

    def __str__(self):
        return '{}|{}'.format(self.name, self.priority_level)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu Setting')
