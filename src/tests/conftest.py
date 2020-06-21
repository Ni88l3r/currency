from django.core.management import call_command

import pytest

from pytest_django.fixtures import _django_db_fixture_helper


@pytest.fixture(scope='session', autouse=True)
def db_session(request, django_db_setup, django_db_blocker):
    if 'django_db_reset_sequences' in request.funcargnames:
        request.getfixturevalue('django_db_reset_sequences')
    if 'transactional_db' in request.funcargnames \
            or 'live_server' in request.funcargnames:
        request.getfixturevalue('transactional_db')
    else:
        _django_db_fixture_helper(request, django_db_blocker, transactional=False)


@pytest.mark.django_db(transaction=True)
@pytest.fixture(scope='session', autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', './tests/fixtures/rates.json')
        call_command('loaddata', './tests/fixtures/users.json')
