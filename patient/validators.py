import re

from django.core.validators import RegexValidator


class PhoneRegexValidator(RegexValidator):
    def __call__(self, value):
        phone_prefix = "+7"
        phone_number_length = "9,15"
        self.message = f"Только телефон (код: {phone_prefix}, " \
                       f"количество цифр: от 9 до 15)"
        regex = r'^\%s\d{%s}$' % (phone_prefix,
                                  phone_number_length)
        self.regex = re.compile(regex, self.flags)
        super().__call__(value)
