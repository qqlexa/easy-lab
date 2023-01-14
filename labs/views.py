import asyncio
import datetime

from asgiref.sync import sync_to_async
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
import piston_rspy

from .models import Laboratory, Language, LaboratoryInLanguage, TestCase

def index(request):
    latest_labs_list = Laboratory.objects.all()
    context = {'latest_labs_list': latest_labs_list}
    return render(request, 'index.html', context)

async def detail(request, laboratory_id):
    laboratory = await get_laboratory(laboratory_id)
    test_cases = await get_laboratory_test_cases(laboratory)
    lab_in_languages = await get_laboratory_available_languages(laboratory)
    languages = await get_languages(lab_in_languages)

    if request.method == 'GET':
        return render(
            request, 'detail.html',
            {'laboratory': laboratory, 'test_cases': test_cases, 'languages': languages}
        )
    else:
        return await send(request, laboratory, test_cases, lab_in_languages, languages)

@sync_to_async
def get_laboratory(laboratory_id: int) -> Laboratory:
    return get_object_or_404(Laboratory, pk=laboratory_id)


@sync_to_async
def get_laboratory_test_cases(laboratory: Laboratory) -> list[TestCase]:
    return list(laboratory.testcase_set.all())


@sync_to_async
def get_laboratory_test_cases(laboratory: Laboratory) -> list[TestCase]:
    return list(laboratory.testcase_set.all())


@sync_to_async
def get_laboratory_available_languages(laboratory: Laboratory) -> list[LaboratoryInLanguage]:
    return list(laboratory.laboratoryinlanguage_set.all())


@sync_to_async
def get_languages(laboratory_available_languages: list[LaboratoryInLanguage]) -> list[Language]:
    return [lil.language for lil in laboratory_available_languages]


@sync_to_async
def get_language_from_laboratory_languages(
        lab_in_languages: list[LaboratoryInLanguage], language_title: str
) -> tuple[LaboratoryInLanguage, Language]:
    lab_in_language = [lil for lil in lab_in_languages if lil.language.title == language_title]
    if len(lab_in_language) == 0:
        raise Http404('Language cannot be empty.')
    elif len(lab_in_language) > 1:
        raise Http404('Language should be only one.')
    lab_in_language = lab_in_language[0]
    language = lab_in_language.language
    return lab_in_language, language


async def send(request, laboratory, test_cases, lab_in_languages, languages):
    user_code = request.POST.get('code', None)
    if user_code is None:
        raise Http404('User code cannot be empty.')

    language_title = request.POST.get('language', None)
    if language_title is None:
        raise Http404('Code language cannot be empty.')

    lab_in_language, language = await get_language_from_laboratory_languages(
        lab_in_languages, language_title
    )

    input_coroutines = []
    for i, test_case in enumerate(test_cases):
        file_content = f'{lab_in_language.code}\n\n{user_code}'
        input_coroutines.append(
            get_file_output(i, file_content, language)
        )

    print(datetime.datetime.now())
    system_cases = await asyncio.gather(*input_coroutines, return_exceptions=True)
    print(datetime.datetime.now())

    counter = 1
    result = {}
    for test_case, system_output in zip(test_cases, system_cases):
        result[f'Test {counter}'] = test_case.expected_output == system_output
        counter += 1

    return render(
        request, 'detail.html',
        {
            'laboratory': laboratory,
            'result': result,
            'test_cases': test_cases,
            'languages': languages,
            'lab_in_languages': lab_in_languages
        }
    )


async def get_file_output(time, file_content: str, language: Language):
    await asyncio.sleep(0.3 * time)

    client = piston_rspy.Client()
    response = await client.execute(
        piston_rspy.Executor()
        .set_language(language.title)
        .add_file(
            piston_rspy.File(
                name="main",
                content=file_content,
            )
        )
    )

    user_output = response.run.output.removesuffix('\n')
    print(f'Language: {response.language} v{response.version}')

    if response.compile:
        print(f'Compilation:\n{response.compile.output}')
    print(f'Output:\n{user_output}')
    return user_output
