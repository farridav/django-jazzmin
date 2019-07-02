# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
