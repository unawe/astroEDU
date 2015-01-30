from django.test import TestCase

from .models import UUIDField


class ArchivalModelTests(TestCase):
    def test_featured(self):
        pass


class UUIDFieldTests(TestCase):

    def test_blank_true(self):
        my_field_instance = UUIDField(blank=True)
        name, path, args, kwargs = my_field_instance.deconstruct()
        new_instance = UUIDField(*args, **kwargs)
        self.assertEqual(my_field_instance.max_length, new_instance.max_length)
        self.assertEqual(my_field_instance.blank, new_instance.blank)

    def test_blank_false(self):
        my_field_instance = UUIDField(blank=False)
        name, path, args, kwargs = my_field_instance.deconstruct()
        new_instance = UUIDField(*args, **kwargs)
        self.assertEqual(my_field_instance.max_length, new_instance.max_length)
        self.assertEqual(my_field_instance.blank, new_instance.blank)

    def test_max_length(self):
        my_field_instance = UUIDField(max_length=77)
        name, path, args, kwargs = my_field_instance.deconstruct()
        new_instance = UUIDField(*args, **kwargs)
        self.assertEqual(my_field_instance.max_length, new_instance.max_length)
        self.assertEqual(my_field_instance.blank, new_instance.blank)
