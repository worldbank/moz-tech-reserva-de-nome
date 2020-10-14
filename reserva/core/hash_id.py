from django.conf import settings
from hashids import Hashids


hash_id = Hashids(
    alphabet=settings.HASH_ID_ALPHABET,
    salt=settings.SECRET_KEY,
    min_length=settings.HASH_ID_MIN_LENGTH,
)
