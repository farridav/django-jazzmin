# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node, InvalidMoveToDescendant, MP_MoveHandler


class Options(models.Model):
    option_name = models.CharField(max_length=255, unique=True, verbose_name=_('Option Name'))
    option_value = models.TextField(verbose_name=_('Option Value'))
    valid = models.BooleanField(default=True, verbose_name=_('Valid'))
    create_time = models.DateTimeField(default=timezone.now, verbose_name=_('CreateTime'))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_('UpdateTime'))

    def __str__(self):
        return f'{self.option_name}'

    @classmethod
    def as_dict(cls):
        return dict(cls.objects.values_list('option_name', 'option_value'))

    class Meta:
        verbose_name = _('Options')
        verbose_name_plural = _('All Options')


class Menu(MP_Node):
    TOP, LEFT = 'top', 'left'
    POSITIONS = (
        (TOP, 'top'),
        (LEFT, 'top'),
    )

    position = models.CharField(max_length=255, default=LEFT, choices=POSITIONS, verbose_name=_('Menu Position'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    link = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Link'),
        help_text=_('support admin:index or /admin/ or http://')
    )
    icon = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Icon'))
    model = models.ForeignKey(
        ContentType, blank=True, null=True, verbose_name=_('ContentType'), on_delete=models.CASCADE,
        help_text=_('Link to the admin page for this model')
    )
    permission = models.ForeignKey(
        Permission, blank=True, null=True, verbose_name=_('ContentType'), on_delete=models.CASCADE,
        help_text=_('use for permission control.')
    )
    priority_level = models.IntegerField(
        default=100, verbose_name=_('Priority Level'), help_text=_('The bigger the priority')
    )
    node_order_by = ['priority_level']

    def clean(self):
        if self.model:
            self.link = reverse(f'admin:{self.model.app_label}_{self.model.model}_changelist')

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
        return f'{self.name}|{self.priority_level}'

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu Setting')
