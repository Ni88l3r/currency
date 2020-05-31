from datetime import date

from celery import shared_task

from rate import model_choices as mch
from rate.models import Rate
from rate.utils import to_decimal

import requests


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    response = response.json()
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }
    for item in response:
        if item['ccy'] not in currency_type_mapper:
            continue
        currency_type = currency_type_mapper[item['ccy']]

        # BUY
        amount = to_decimal(item['buy'])
        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        # SALE
        amount = to_decimal(item['sale'])
        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response = response.json()
    currency_type_mapper = {
        840: mch.CURRENCY_TYPE_USD,
        978: mch.CURRENCY_TYPE_EUR,
    }
    for item in response:
        if item == 'errorDescription' \
                or item['currencyCodeB'] != 980 \
                or item['currencyCodeA'] not in currency_type_mapper:
            continue
        currency_type = currency_type_mapper[item['currencyCodeA']]
        # BUY
        amount = to_decimal(item['rateBuy'])
        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )
        # SALE
        amount = to_decimal(item['rateSell'])
        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    response = response.json()
    currency_type_mapper = {
        'Dollar': mch.CURRENCY_TYPE_USD,
        'Euro': mch.CURRENCY_TYPE_EUR,
    }
    for item in response:
        if item not in currency_type_mapper:
            continue
        currency_type = currency_type_mapper[item]
        # BUY
        amount = to_decimal(response[item]['buy'][:4])
        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )
        # SALE
        amount = to_decimal(response[item]['sale'][:4])
        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_nbu():
    current_date = date.today().strftime("%Y%m%d")
    url = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={current_date}&json'
    response = requests.get(url)
    response = response.json()
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }
    for item in response:
        if item['cc'] not in currency_type_mapper:
            continue
        currency_type = currency_type_mapper[item['cc']]
        # BUY
        amount = to_decimal(item['rate'])
        last = Rate.objects.filter(
            source=mch.SOURCE_NBU,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_NBU,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )
        # SALE
        amount = to_decimal(item['rate'])
        last = Rate.objects.filter(
            source=mch.SOURCE_NBU,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_NBU,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_otpbank():
    current_date = date.today().strftime("%d.%m.%Y")
    url = f'https://ru.otpbank.com.ua/local/components/otp/utils.exchange_rate_arc/exchange_rate_by_date.php' \
          f'?curr_date={current_date}&ib_code=otp_bank_currency_rates'
    response = requests.get(url)
    response = response.json()
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }
    for item in response['items']:
        if item['NAME'] not in currency_type_mapper:
            continue
        currency_type = currency_type_mapper[item['NAME']]

        # BUY
        amount = to_decimal(item['BUY'])
        last = Rate.objects.filter(
            source=mch.SOURCE_OTPBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_OTPBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        # SALE
        amount = to_decimal(item['SELL'])
        last = Rate.objects.filter(
            source=mch.SOURCE_OTPBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_OTPBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_tascombank():
    url = 'https://tascombank.ua/api/currencies'
    response = requests.get(url)
    response = response.json()
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }
    for item in response[0]:
        if item['short_name'] not in currency_type_mapper or item['kurs_type_description'] != 'Обменный':
            continue
        currency_type = currency_type_mapper[item['short_name']]

        # BUY
        amount = to_decimal(item['kurs_buy'])
        last = Rate.objects.filter(
            source=mch.SOURCE_TASCOMBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_TASCOMBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        # SALE
        amount = to_decimal(item['kurs_sale'])
        last = Rate.objects.filter(
            source=mch.SOURCE_TASCOMBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_TASCOMBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse():
    parse_monobank.delay()
    parse_privatbank.delay()
    parse_vkurse.delay()
    parse_nbu.delay()
    parse_otpbank.delay()
    parse_tascombank.delay()
