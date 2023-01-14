import asyncio
import datetime

from asgiref.sync import sync_to_async
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
import piston_rspy

from .models import Laboratory, TestCase

def index(request):
    latest_labs_list = Laboratory.objects.order_by('-pub_date')[:5]
    context = {'latest_labs_list': latest_labs_list}
    return render(request, 'index.html', context)

async def detail(request, laboratory_id):
    laboratory = await get_laboratory(laboratory_id)
    test_cases = await get_laboratory_test_cases(laboratory)
    if request.method == 'GET':
        test_cases_result = []
        for test_case in test_cases:
            result = (test_case, None)
            test_cases_result.append(result)
        return render(
            request, 'detail.html',
            {'laboratory': laboratory, 'test_cases': test_cases, 'test_cases_result': test_cases_result}
        )
    else:
        return await send(request, laboratory, test_cases)

@sync_to_async
def get_laboratory(laboratory_id: int) -> Laboratory:
    return get_object_or_404(Laboratory, pk=laboratory_id)


@sync_to_async
def get_laboratory_test_cases(laboratory: Laboratory) -> list[TestCase]:
    return list(laboratory.testcase_set.all())


async def send(request, laboratory, test_cases):
    user_code = request.POST.get('code', None)
    if user_code is None:
        raise Http404('User code cannot be empty.')

    result = {}
    input_coroutines = []
    for i, test_case in enumerate(test_cases):
        file_content = f'{test_case.case_input}\n\n{user_code}'
        # await
        input_coroutines.append(get_file_output(i, file_content))
    print(datetime.datetime.now())
    system_cases = await asyncio.gather(*input_coroutines, return_exceptions=True)
    print(datetime.datetime.now())

    test_cases_result = []
    for test_case, system_output in zip(test_cases, system_cases):
        result = (test_case, test_case.case_output == system_output)
        test_cases_result.append(result)

    return render(request, 'detail.html', {'laboratory': laboratory, 'test_cases': test_cases, 'test_cases_result': test_cases_result})


async def get_file_output(time, file_content):
    await asyncio.sleep(0.3 * time)
    file = piston_rspy.File(
        name='main.py',
        content=file_content,
    )

    executor = piston_rspy.Executor(
        language='python',  # TODO: Add choice of languages
        version='3.10',
        files=[file],
    )

    client = piston_rspy.Client()
    response = await client.execute(executor)

    user_output = response.run.output.removesuffix('\n')
    print(f'Language: {response.language} v{response.version}')

    if response.compile:
        print(f'Compilation:\n{response.compile.output}')
    print(f'Output:\n{user_output}')
    return user_output
