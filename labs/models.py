from django.db import models


class Laboratory(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f'{self.title}\n\n{self.description}'


class TestCase(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)  # 1 laboratory -> * laboratory tests

    description = models.CharField(max_length=200)  # description about this test
    case_input = models.CharField(max_length=1000)  # input from system
    case_output = models.CharField(max_length=1000)  # expected student output


class UserAnswer(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)  # 1 laboratory -> * user answers
    # TODO: user = models.ForeignKey(User, on_delete=models.CASCADE)  # user laboratory -> * user answers

    code = models.CharField(max_length=5000)
    upload_date = models.DateTimeField('date uploaded')
