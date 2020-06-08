from datetime import date, timedelta

from django.core.management.base import BaseCommand

from rate import model_choices as mch
from rate.models import Rate
from rate.utils import to_decimal

import requests


class Command(BaseCommand):
    # noqa django requires
    help = 'Parse PrivatBank exchange archive. Require 2 arguments: "start" and "end" date of interval in DD.MM.YYYY format. Example: parse_privatbank 01.11.2014 02.12.2014' # noqa django requires

    def add_arguments(self, parser):
        parser.add_argument('start', type=str, help='The start interval of dates to be parsed (DD.MM.YYYY).')
        parser.add_argument('end', type=str, help='The end interval of dates to be parsed (DD.MM.YYYY).')

    def handle(self, *args, **kwargs):
        def parse(day_to_parse):
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={day_to_parse.strftime("%d.%m.%Y")}'
            response = requests.get(url)
            response = response.json()
            currency_type_mapper = {
                'USD': mch.CURRENCY_TYPE_USD,
                'EUR': mch.CURRENCY_TYPE_EUR,
            }
            for item in response['exchangeRate']:
                if item['currency'] not in currency_type_mapper:
                    continue
                currency_type = currency_type_mapper[item['currency']]
                # BUY
                amount = to_decimal(item['purchaseRate'])
                last = Rate.objects.filter(
                    source=mch.SOURCE_PRIVATBANK,
                    currency_type=currency_type,
                    type=mch.RATE_TYPE_BUY,
                ).last()
                if last is None or last.amount != amount:
                    Rate.objects.create(
                        created=day_to_parse,
                        amount=amount,
                        source=mch.SOURCE_PRIVATBANK,
                        currency_type=currency_type,
                        type=mch.RATE_TYPE_BUY,
                    )
                # SALE
                amount = to_decimal(item['saleRate'])
                last = Rate.objects.filter(
                    source=mch.SOURCE_PRIVATBANK,
                    currency_type=currency_type,
                    type=mch.RATE_TYPE_SALE,
                ).last()
                if last is None or last.amount != amount:
                    Rate.objects.create(
                        created=day_to_parse,
                        amount=amount,
                        source=mch.SOURCE_PRIVATBANK,
                        currency_type=currency_type,
                        type=mch.RATE_TYPE_SALE,
                    )

        start_day = int(kwargs['start'][:2])
        start_month = int(kwargs['start'][3:5])
        start_year = int(kwargs['start'][6:10])
        end_day = int(kwargs['end'][:2])
        end_month = int(kwargs['end'][3:5])
        end_year = int(kwargs['end'][6:10])
        start = date(start_year, start_month, start_day)
        end = date(end_year, end_month, end_day)
        delta = end - start

        for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            parse(day)
            self.stdout.write(f'Parsed date: {day.strftime("%d.%m.%Y")}.')
        self.stdout.write(f'Complete! Parsed interval: {kwargs["start"]} - {kwargs["end"]}.')
