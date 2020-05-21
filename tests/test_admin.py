import random

import pytest
from django.utils import timezone

from jazzmin.compat import reverse
from tests.test_app.polls.models import Poll, Vote, Choice


@pytest.fixture
def test_data(transactional_db, admin_user):
    dataset = {
        'How much cheese can you eat?': ['loads', 'some', 'all of it'],
        'Whats bigger than an elephant?': ['dog', 'a bigger elephant', 'mouldy cabbage']
    }

    polls = []
    for question, answers in dataset.items():
        poll = Poll.objects.create(owner=admin_user, text=question, pub_date=timezone.now())

        choices = []
        for answer in answers:
            choices.append(Choice.objects.create(poll=poll, choice_text=answer))

        for x in range(1, random.randint(2, 10)):
            Vote.objects.create(user=admin_user, poll=poll, choice=random.choice(choices))

        polls.append(poll)

    return polls


####################
# Main admin views #
####################
@pytest.mark.django_db
def test_login(client):
    url = reverse('admin:login')

    response = client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert templates_used == ['admin/login.html']


@pytest.mark.django_db
def test_logout(admin_client):
    url = reverse('admin:logout')

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert templates_used == ['registration/logged_out.html']


@pytest.mark.django_db
def test_password_change(admin_client):
    url = reverse('admin:password_change')

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert set(templates_used) == {
        'admin/base.html',
        'admin/base_site.html',
        'django/forms/widgets/attrs.html',
        'django/forms/widgets/input.html',
        'django/forms/widgets/password.html',
        'registration/password_change_form.html'
    }

    response = admin_client.post(url, data={
        'old_password': 'password',
        'new_password1': 'PickleRick123!!',
        'new_password2': 'PickleRick123!!'
    }, follow=True)
    templates_used = [t.name for t in response.templates]

    assert 'Password change successful' in response.content.decode()
    assert set(templates_used) == {
        'registration/password_change_done.html',
        'admin/base.html',
        'admin/base_site.html'
    }


@pytest.mark.django_db
def test_dashboard(admin_client):
    url = reverse('admin:index')

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    assert templates_used == ['admin/index.html', 'admin/base_site.html', 'admin/base.html']


##############################
# Admin views for our models #
##############################

@pytest.mark.django_db
def test_detail(admin_client, test_data):
    url = reverse('admin:polls_poll_change', args=(test_data[0].pk,))

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    render_counts = {x: templates_used.count(x) for x in set(templates_used)}

    # The number of times each template was rendered
    assert render_counts == {
        'admin/base.html': 1,
        'admin/base_site.html': 1,
        'admin/change_form.html': 1,
        'admin/change_form_object_tools.html': 1,
        'admin/edit_inline/tabular.html': 1,
        'admin/includes/fieldset.html': 2,
        'admin/prepopulated_fields_js.html': 1,
        'admin/submit_line.html': 2,
        'admin/widgets/foreign_key_raw_id.html': 1,
        'admin/widgets/split_datetime.html': 1,
        'django/forms/widgets/attrs.html': 35,
        'django/forms/widgets/checkbox.html': 4,
        'django/forms/widgets/date.html': 2,
        'django/forms/widgets/hidden.html': 18,
        'django/forms/widgets/input.html': 34,
        'django/forms/widgets/multiwidget.html': 1,
        'django/forms/widgets/splithiddendatetime.html': 1,
        'django/forms/widgets/text.html': 7,
        'django/forms/widgets/textarea.html': 1,
        'django/forms/widgets/time.html': 2
    }

    # The templates that were used
    assert set(templates_used) == {
        'admin/base.html',
        'admin/base_site.html',
        'admin/change_form.html',
        'admin/change_form_object_tools.html',
        'admin/edit_inline/tabular.html',
        'admin/includes/fieldset.html',
        'admin/prepopulated_fields_js.html',
        'admin/submit_line.html',
        'admin/widgets/foreign_key_raw_id.html',
        'admin/widgets/split_datetime.html',
        'django/forms/widgets/attrs.html',
        'django/forms/widgets/checkbox.html',
        'django/forms/widgets/date.html',
        'django/forms/widgets/hidden.html',
        'django/forms/widgets/input.html',
        'django/forms/widgets/multiwidget.html',
        'django/forms/widgets/splithiddendatetime.html',
        'django/forms/widgets/text.html',
        'django/forms/widgets/textarea.html',
        'django/forms/widgets/time.html'
    }

    # TODO: post data and confirm we can change model instances

@pytest.mark.django_db
def test_list(admin_client, test_data):
    url = reverse('admin:polls_poll_changelist')

    response = admin_client.get(url)
    templates_used = [t.name for t in response.templates]

    assert response.status_code == 200
    render_counts = {x: templates_used.count(x) for x in set(templates_used)}

    # The number of times each template was rendered
    assert render_counts == {
        'admin/actions.html': 2,
        'admin/base.html': 1,
        'admin/base_site.html': 1,
        'admin/change_list.html': 1,
        'admin/change_list_object_tools.html': 1,
        'admin/change_list_results.html': 1,
        'admin/date_hierarchy.html': 1,
        'admin/filter.html': 1,
        'admin/pagination.html': 1,
        'admin/search_form.html': 1,
        'django/forms/widgets/attrs.html': 18,
        'django/forms/widgets/checkbox.html': 4,
        'django/forms/widgets/hidden.html': 8,
        'django/forms/widgets/input.html': 12,
        'django/forms/widgets/select.html': 2,
        'django/forms/widgets/select_option.html': 4
    }

    # The templates that were used
    assert set(templates_used) == {
        'admin/actions.html',
        'admin/base.html',
        'admin/base_site.html',
        'admin/change_list.html',
        'admin/change_list_object_tools.html',
        'admin/change_list_results.html',
        'admin/date_hierarchy.html',
        'admin/filter.html',
        'admin/pagination.html',
        'admin/search_form.html',
        'django/forms/widgets/attrs.html',
        'django/forms/widgets/checkbox.html',
        'django/forms/widgets/hidden.html',
        'django/forms/widgets/input.html',
        'django/forms/widgets/select.html',
        'django/forms/widgets/select_option.html'
    }


@pytest.mark.django_db
def test_history():
    pass


@pytest.mark.django_db
def test_delete():
    pass
