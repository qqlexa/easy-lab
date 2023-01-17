from django import forms

from .models import Laboratory, Subject, Language, TestCase, LaboratoryInLanguage


class LaboratoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].empty_label = "Subject is not selected"

    class Meta:
        model = Laboratory
        fields = ['title', 'description', 'pub_date', 'subject']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 20})
        }


# class TestCaseForm(forms.ModelForm):
#     class Meta:
#         model = TestCase
#
#     fields = ['description', 'description_input', 'description_output', 'expected_output']
#     widgets = {
#         'description': forms.Textarea(attrs={'cols': 60, 'rows': 20})
#     }
#
#
# class LaboratoryInLanguageForm(forms.ModelForm):
#     class Meta:
#         model = LaboratoryInLanguage
#
#     fields = ['code']
######
    # laboratory = models.ForeignKey(
    #     Laboratory, on_delete=models.CASCADE
    # )  # 1 laboratory -> * laboratory in language
    # language = models.ForeignKey(
    #     Language, on_delete=models.CASCADE
    # )  # 1 language -> * laboratory in language
    # test_case = models.ForeignKey(
    #     TestCase, on_delete=models.CASCADE
    # )  # 1 test_case -> * laboratory in language
    #
    # code = models.CharField(max_length=200)  # code that runs before user code
