"""Forms testing module."""

from typing import Iterable

from django.test import TestCase

from freelance import forms

DIGIT = '9'
PWD1 = 'password1'


def add_tests(test_attrs: tuple):
    """
    Decorate the function for appending new tests.

    Args:
        test_attrs: attrs for testing.

    Returns:
        decorator: class decorator.
    """
    def decorator(class_):
        """
        Decorate the class.

        Args:
            class_: class to decorate.

        Returns:
            decorator: decorated class.
        """
        for num, output_data in enumerate(test_attrs):
            atributes, new_value = output_data

            def new_test(self):
                copied = self._valid_data.copy()
                if isinstance(atributes, Iterable):
                    for attr in atributes:
                        copied[attr] = new_value
                else:
                    copied[atributes] = new_value
                self.assertFalse(forms.RegistrationForm(data=copied).is_valid())

            setattr(
                class_,
                'test_{0}_{1}'.format(
                    atributes[0] if isinstance(atributes, Iterable) else atributes,
                    num,
                ),
                new_test,
            )
        return class_
    return decorator


registration_tests = (
    ('username', ''),
    ('email', '123'),
    ([PWD1, 'password2'], DIGIT * 7),
    (PWD1, '2h3ru9rhg083hf920h'),
    ([PWD1, 'password2'], 'Abcdef123'),
)


@add_tests(registration_tests)
class TestRegistrationForm(TestCase):
    """Class for registration tests."""

    _valid_data = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'username@sirius.ru',
        PWD1: 'ALsk1029!',
        'password2': 'ALsk1029!',
    }

    def test_successful(self):
        """Provide sucessful tests."""
        form = forms.RegistrationForm(data=self._valid_data)
        self.assertTrue(form.is_valid())
