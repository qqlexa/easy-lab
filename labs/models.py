from django.db import models


class Laboratory(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')


class Language(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)  # Title that user see


class LaboratoryInLanguage(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)  # 1 laboratory -> * laboratory in language
    language = models.ForeignKey(Language, on_delete=models.CASCADE)  # 1 language -> * laboratory in language

    code = models.CharField(max_length=200)  # code that runs before user code


class TestCase(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)  # 1 laboratory -> * laboratory tests

    description = models.CharField(max_length=200)  # description about this test
    description_input = models.CharField(max_length=1000)  # example input
    description_output = models.CharField(max_length=1000)  # example output
    expected_output = models.CharField(max_length=1000)  # expected student output


# class UserAnswer(models.Model):
#     laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)  # 1 laboratory -> * user answers
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)  # 1 language -> * user answers
#     # TODO: user = models.ForeignKey(User, on_delete=models.CASCADE)  # user laboratory -> * user answers
#
#     code = models.CharField(max_length=5000)
#     upload_date = models.DateTimeField('date uploaded')
