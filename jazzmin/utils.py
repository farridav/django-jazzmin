import logging

from django.urls import reverse, NoReverseMatch

logger = logging.getLogger(__name__)


def order_with_respect_to(first, reference):
    ranking = []
    max_num = len(first)

    for item in first:
        try:
            pos = reference.index(item['app_label'])
        except ValueError:
            pos = max_num

        ranking.append(pos)

    return [y for x, y in sorted(zip(ranking, first), key=lambda x: x[0])]


def get_admin_url(model):
    """
    Return the admin URL for the given <app>.<model>
    """
    try:
        app_label, model_name = model.split('.')
        return reverse(f"admin:{app_label}_{model_name}_changelist")
    except NoReverseMatch:
        logger.error(f'Could not reverse {model}, it must be in <app_label>.<model_name> format')
        return None


def get_filter_id(spec):
    return getattr(spec, 'field_path', getattr(spec, 'parameter_name', spec.title))
