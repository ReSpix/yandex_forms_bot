import asyncio
import asana
from asana.rest import ApiException
import logging


configuration = None
api_client = None


def init():
    global configuration
    global api_client
    configuration = asana.Configuration()
    configuration.access_token = '2/1209973749938053/1209975213456219:b98001676e7b3db5863ccf056a56bb2f'
    api_client = asana.ApiClient(configuration)


def put_to_section(task_gid):
    sections_api_instance = asana.SectionsApi(api_client)
    section_gid = "1209973648210834"
    opts = {
        'body': {"data": {"task": task_gid}},
    }
    try:
        section = sections_api_instance.add_task_for_section(section_gid, opts)
        logging.info(f"Задача {task_gid} установлена в секцию {section_gid}")
    except ApiException as e:
        logging.warning(
            f"Ошибка перемещения задачи {task_gid} в секцию {section_gid}: {e}")


def _publish_asana_task(text: str):
    if api_client is None:
        init()
    tasks_api_instance = asana.TasksApi(api_client)
    body = {
        "data": {
            "name": f"Новое распределение",
            "projects": ["1209973648210833"],
            "notes": text
        }
    }
    opts = {}

    try:
        task = tasks_api_instance.create_task(body, opts)
        if not isinstance(task, dict):
            return
        put_to_section(task['gid'])
    except ApiException as e:
        logging.info("Exception when calling TasksApi->create_task: %s\n" % e)


async def publish_asana_task(text: str):
    loop = asyncio.get_running_loop()
    # По умолчанию используется ThreadPoolExecutor
    return await loop.run_in_executor(None, _publish_asana_task, text)