from django.db import models


class Laboratory(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')


class Language(models.Model):
    title = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=30)  # Title that user see


class TestCase(models.Model):
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE
    )  # 1 laboratory -> * laboratory tests

    description = models.CharField(max_length=200)  # description about this test
    description_input = models.CharField(max_length=1000)  # example input
    description_output = models.CharField(max_length=1000)  # example output
    expected_output = models.CharField(max_length=1000)  # expected student output


class LaboratoryInLanguage(models.Model):
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE
    )  # 1 laboratory -> * laboratory in language
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE
    )  # 1 language -> * laboratory in language
    test_case = models.ForeignKey(
        TestCase, on_delete=models.CASCADE
    )  # 1 test_case -> * laboratory in language

    code = models.CharField(max_length=200)  # code that runs before user code


# class UserAnswer(models.Model):
#     laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)  # 1 laboratory -> * user answers
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)  # 1 language -> * user answers
#     # TODO: user = models.ForeignKey(User, on_delete=models.CASCADE)  # user laboratory -> * user answers
#
#     code = models.CharField(max_length=5000)
#     upload_date = models.DateTimeField('date uploaded')

# python manage.py makemigrations labs
# python manage.py migrate
# python manage.py shell
# from labs.models import *
# from django.utils import timezone
# lab = Laboratory(title='Lab', description='descr', pub_date=timezone.now())
# lab.save()
# python = Language(title='python', description='Python')
# js = Language(title='js', description='JavaS')
# cpp = Language(title='cpp', description='C++')
# python.save()
# js.save()
# cpp.save()
# tc = TestCase(laboratory=lab, description='description2', description_input='case_input2', description_output='case_output2', expected_output='1')
# tc.save()
# lil_cpp = LaboratoryInLanguage(laboratory=lab, language=cpp, test_case=tc, code='string text="1";')
# lil_js = LaboratoryInLanguage(laboratory=lab, language=js, test_case=tc, code='text=1')
# lil_python = LaboratoryInLanguage(laboratory=lab, language=python, test_case=tc, code='text=1')
# lil_cpp.save()
# lil_python.save()
# lil_js.save()
# tc2 = TestCase(laboratory=lab, description='description_hello', description_input='hello', description_output='hello', expected_output='Hello world!')
# tc2.save()
# lil2_python = LaboratoryInLanguage(laboratory=lab, language=python, test_case=tc, code='text="Hello world!"')
# lil2_js = LaboratoryInLanguage(laboratory=lab, language=js, test_case=tc, code='text="Hello world!"')
# lil2_cpp = LaboratoryInLanguage(laboratory=lab, language=cpp, test_case=tc, code='string text="Hello world!";')
# lil2_python.save()
# lil2_js.save()
# lil2_cpp.save()
