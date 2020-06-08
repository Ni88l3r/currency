import hashlib
from django.core.cache import cache

from rate.models import Rate
from rate import model_choices as mch


def rate_cache_key(source, type_, currency) -> str:
    return hashlib.md5(
        f'RATES-LATEST_{source}_{type_}_{currency}'.encode()
    ).hexdigest()


def get_latest_rates():
    object_list = []
    for source in mch.SOURCE_CHOICES:  # source
        source = source[0]
        for currency in mch.CURRENCY_TYPE_CHOICES:  # currency_type
            currency = currency[0]
            for type_ in mch.RATE_TYPE_CHOICES:  # type
                type_ = type_[0]
                key = rate_cache_key(source, type_, currency)
                cached_rate = cache.get(key)
                # no rate in cache
                if cached_rate is None:
                    rate = Rate.objects.filter(
                        source=source,
                        type=type_,
                        currency_type=currency,
                    ).last()
                    if rate is not None:
                        cache.set(key, rate, 30)
                        object_list.append(rate)
                else:  # value in cache
                    object_list.append(cached_rate)
    return object_list
