from account.models import Contact

from django.core import mail
from django.urls import reverse


def test_contact_us_get_form(client):
    url = reverse('account:contact-us')
    response = client.get(url)
    assert response.status_code == 200


def test_contact_us_empty_payload(client):
    assert len(mail.outbox) == 0
    initial_count = Contact.objects.count()
    url = reverse('account:contact-us')
    response = client.post(url, {})
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 3
    assert errors['email_from'] == ['Обязательное поле.']
    assert errors['title'] == ['Обязательное поле.']
    assert errors['message'] == ['Обязательное поле.']
    assert Contact.objects.count() == initial_count
    assert len(mail.outbox) == 0


def test_contact_us_incorrect_payload(client):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0

    url = reverse('account:contact-us')
    payload = {
        'email_from': 'mailmail',
        'title': 'hello world',
        'message': 'hello world\n' * 50,
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['email_from'] == ['Введите правильный адрес электронной почты.']
    assert Contact.objects.count() == initial_count
    assert len(mail.outbox) == 0


def test_contact_us_correct_payload(client, settings):
    initial_count = Contact.objects.count()
    assert len(mail.outbox) == 0

    url = reverse('account:contact-us')
    payload = {
        'email_from': 'mailmail@mail.com',
        'title': 'hello world',
        'message': 'hello world' * 50,
    }
    response = client.post(url, payload)
    assert response.status_code == 302
    assert response.url == reverse('index')
    assert Contact.objects.count() == initial_count + 1

    # check email
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.subject == payload['title']
    assert email.body == payload['message']
    assert email.from_email == payload['email_from']
    assert email.to == [settings.DEFAULT_FROM_EMAIL]


def test_login_page_availability(client):
    url = reverse('account:login')
    response = client.get(url)
    assert response.status_code == 200


def test_login_empty_payload(client):
    url = reverse('account:login')
    response = client.post(url, {})
    errors = response.context_data['form'].errors
    assert len(errors) == 2
    assert errors['username'] == ['Обязательное поле.']
    assert errors['password'] == ['Обязательное поле.']


def test_login_page_incorrect_payload(client):
    url = reverse('account:login')
    payload = {
        'username': 'false_username',
        'password': 'false_password',
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    errors = response.context_data['form'].errors
    assert len(errors) == 1
    assert errors['__all__'] == ['Пожалуйста, введите правильные имя пользователя и пароль.'
                                 ' Оба поля могут быть чувствительны к регистру.']


def test_login_page_correct_payload(client):
    url = reverse('account:login')
    payload = {
        'username': 'admin_user',
        'password': 'admin_user',
    }
    response = client.post(url, payload)
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated is True
    assert response.wsgi_request.user.username == 'admin_user'
    assert response.wsgi_request.user.pk == 1
    assert response.wsgi_request.user.is_superuser is True
    assert response.wsgi_request.user.is_staff is True
    assert response.url == reverse('index')


def test_logout_page_availability(admin_client):
    url = reverse('account:logout')
    response = admin_client.get(url)
    assert response.wsgi_request.user.is_authenticated is False
    assert response.status_code == 302
    assert response.url == reverse('index')
