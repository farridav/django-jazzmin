import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from tests.utils import parse_sidemenu, user_with_permissions, parse_topmenu, parse_usermenu


@pytest.mark.django_db
def test_side_menu(admin_client, settings):
    """
    All menu tweaking settings work as expected
    """
    url = reverse('admin:index')

    response = admin_client.get(url)

    assert parse_sidemenu(response) == {
        'Global': ['/admin/'],
        'Polls': ['/admin/polls/choice/', '/admin/polls/poll/', '/admin/polls/vote/', '/make_messages/'],
        'Administration': ['/admin/admin/logentry/'],
        'Authentication and Authorization': ['/admin/auth/group/', '/admin/auth/user/']
    }

    settings.JAZZMIN_SETTINGS['hide_models'] = ['auth.user']
    response = admin_client.get(url)

    assert parse_sidemenu(response) == {
        'Global': ['/admin/'],
        'Polls': ['/admin/polls/choice/', '/admin/polls/poll/', '/admin/polls/vote/', '/make_messages/'],
        'Administration': ['/admin/admin/logentry/'],
        'Authentication and Authorization': ['/admin/auth/group/']
    }


@pytest.mark.django_db
def test_update_site_logo(admin_client, settings):
    """
    We can add a site logo, and it renders out
    """
    url = reverse('admin:index')

    settings.JAZZMIN_SETTINGS['site_logo'] = 'polls/img/logo.png'
    response = admin_client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.find('a', class_="brand-link").find('img')['src'] == '/static/polls/img/logo.png'


@pytest.mark.django_db
def test_permissions_on_custom_links(client, settings):
    """
    we honour permissions for the rendering of custom links
    """
    user = user_with_permissions()
    user2 = user_with_permissions('polls.view_poll')

    url = reverse('admin:index')

    settings.JAZZMIN_SETTINGS['custom_links'] = {
        'polls': [{
            'name': 'Make Messages', 'url': 'make_messages',
            'icon': 'fa-comments', 'permissions': ['polls.view_poll']
        }]
    }

    client.force_login(user)
    response = client.get(url)
    assert parse_sidemenu(response) == {'Global': ['/admin/']}

    client.force_login(user2)
    response = client.get(url)
    assert parse_sidemenu(response) == {'Global': ['/admin/'], 'Polls': ['/admin/polls/poll/', '/make_messages/']}


@pytest.mark.django_db
def test_top_menu(admin_client, settings):
    """
    Top menu renders out as expected
    """
    url = reverse('admin:index')

    settings.JAZZMIN_SETTINGS['topmenu_links'] = [
        {'name': 'Home', 'url': 'admin:index', 'permissions': ['auth.view_user']},
        {'name': 'Support', 'url': 'https://github.com/farridav/django-jazzmin/issues', 'new_window': True},
        {'model': 'auth.User'},
        {'app': 'polls'},
    ]

    response = admin_client.get(url)

    assert parse_topmenu(response) == [
        {'name': 'Home', 'link': '/admin/'},
        {'name': 'Support', 'link': 'https://github.com/farridav/django-jazzmin/issues'},
        {'name': 'Users', 'link': '/admin/auth/user/'},
        {'name': 'Polls', 'link': '#', 'children': [
            {'name': 'Polls', 'link': '/admin/polls/poll/'},
            {'name': 'Choices', 'link': '/admin/polls/choice/'},
            {'name': 'Votes', 'link': '/admin/polls/vote/'},
        ]}
    ]


@pytest.mark.django_db
def test_user_menu(admin_user, client, settings):
    """
    The User menu renders out as expected
    """
    url = reverse('admin:index')

    settings.JAZZMIN_SETTINGS['usermenu_links'] = [
        {'name': 'Home', 'url': 'admin:index', 'permissions': ['auth.view_user']},
        {'name': 'Support', 'url': 'https://github.com/farridav/django-jazzmin/issues', 'new_window': True},
        {'model': 'auth.User'},
    ]

    client.force_login(admin_user)
    response = client.get(url)

    assert parse_usermenu(response) == [
        {'link': '/admin/password_change/', 'name': 'Change password'},
        {'link': '/admin/logout/', 'name': 'Log out'},
        {'link': '/admin/auth/user/{}/change/'.format(admin_user.pk), 'name': 'See Profile'},
        {'link': '/admin/', 'name': 'Home'},
        {'link': 'https://github.com/farridav/django-jazzmin/issues', 'name': 'Support'},
        {'link': '/admin/auth/user/', 'name': 'Users'}
    ]
