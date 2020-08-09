import random

from django.urls import reverse
from django.utils import timezone

from rate.models import Rate


def test_rate_list(client):
    url = reverse('rate:list')
    response = client.get(url)
    assert response.status_code == 200


def test_rate_csv(client):
    url = reverse('rate:download-csv')
    response = client.get(url)
    assert response.status_code == 200
    assert response._headers['content-type'] == ('Content-Type', 'text/csv')
    assert response._headers['content-disposition'][1][:11] == 'attachment;'


def test_rate_xlsx(client):
    url = reverse('rate:download-xlsx')
    response = client.get(url)
    assert response.status_code == 200
    assert response._headers['content-type'] == ('Content-Type', 'text/xlsx')
    assert response._headers['content-disposition'][1][:11] == 'attachment;'


def test_rate_latest(client):
    url = reverse('rate:latest')
    response = client.get(url)
    assert response.status_code == 200


def test_edit_rate_anon_user(client):
    pk = Rate.objects.last().id
    url = reverse('rate:edit', args=(pk,))
    response = client.get(url)
    assert response.status_code == 302


def test_edit_rate_common_user(client):
    url = reverse('account:login')
    payload = {
        'username': 'common_user',
        'password': 'common_user',
    }
    response = client.post(url, payload)
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated is True
    assert response.wsgi_request.user.username == 'common_user'
    assert response.wsgi_request.user.is_superuser is False
    assert response.wsgi_request.user.is_staff is False
    pk = Rate.objects.last().id
    url = reverse('rate:edit', args=(pk,))
    response = client.get(url)
    assert response.status_code == 403


def test_edit_rate_admin_form_availability(admin_client):
    pk = Rate.objects.last().id
    url = reverse('rate:edit', args=(pk,))
    response = admin_client.get(url)
    assert response.status_code == 200
    assert len(response.context_data['form'].fields.items()) == 5


def test_edit_rate_admin_empty_payload(admin_client):
    pk = Rate.objects.last().id
    url = reverse('rate:edit', args=(pk,))
    response = admin_client.post(url, {})
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 5
    assert errors['created'] == ['Это поле обязательно.']
    assert errors['amount'] == ['Это поле обязательно.']
    assert errors['source'] == ['Это поле обязательно.']
    assert errors['currency_type'] == ['Это поле обязательно.']
    assert errors['type'] == ['Это поле обязательно.']


def test_edit_rate_admin_incorrect_payload(admin_client):
    pk = Rate.objects.last().id
    url = reverse('rate:edit', args=(pk,))
    payload = {
        'created': 'wrong_data',
        'amount': 'wrong_data',
        'source': 'wrong_data',
        'currency_type': 'wrong_data',
        'type': 'wrong_data',
    }
    response = admin_client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 5
    assert errors['created'] == ['Введите правильную дату и время.']
    assert errors['amount'] == ['Введите число.']
    assert errors['source'] == ['Выберите корректный вариант. wrong_data нет среди допустимых значений.']
    assert errors['currency_type'] == ['Выберите корректный вариант. wrong_data нет среди допустимых значений.']
    assert errors['type'] == ['Выберите корректный вариант. wrong_data нет среди допустимых значений.']


def test_edit_rate_admin_correct_payload(admin_client):
    pk = Rate.objects.last().id
    url = reverse('rate:edit', args=(pk,))
    time_zone = timezone.get_default_timezone()
    payload = {
        'created': str(timezone.now().astimezone(time_zone).strftime("%d.%m.%Y %H:%M:%S")),
        'amount': random.randint(10, 30),
        'source': random.randint(1, 6),
        'currency_type': random.randint(1, 2),
        'type': random.randint(1, 2),
    }
    response = admin_client.post(url, payload)
    assert response.status_code == 302
    assert Rate.objects.last().amount == payload['amount']
    assert Rate.objects.last().source == payload['source']
    assert Rate.objects.last().currency_type == payload['currency_type']
    assert Rate.objects.last().type == payload['type']


def test_delete_rate_anon_user(client):
    count_before = Rate.objects.all().count()
    pk = Rate.objects.last().id
    url = reverse('rate:delete', args=(pk,))
    response = client.get(url)
    count_after = Rate.objects.all().count()
    assert response.status_code == 302
    assert count_before == count_after


def test_delete_rate_common_user(client):
    url = reverse('account:login')
    payload = {
        'username': 'common_user',
        'password': 'common_user',
    }
    response = client.post(url, payload)
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated is True
    assert response.wsgi_request.user.username == 'common_user'
    assert response.wsgi_request.user.is_superuser is False
    assert response.wsgi_request.user.is_staff is False
    count_before = Rate.objects.all().count()
    pk = Rate.objects.last().id
    url = reverse('rate:delete', args=(pk,))
    response = client.get(url)
    count_after = Rate.objects.all().count()
    assert response.status_code == 403
    assert count_before == count_after


def test_delete_rate_admin(admin_client):
    count_before = Rate.objects.all().count()
    pk = Rate.objects.last().id
    url = reverse('rate:delete', args=(pk,))
    response = admin_client.get(url)
    count_after = Rate.objects.all().count()
    assert response.status_code == 302
    assert response.url == reverse('rate:list')
    assert count_before == count_after + 1
