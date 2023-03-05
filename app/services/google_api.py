from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
SPREADSHEET_BODY = {
    'properties': {
        'locale': 'ru_RU',
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {'rowCount': 100, 'columnCount': 11},
            }
        }
    ],
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    json = SPREADSHEET_BODY
    json['properties']['title'] = f'Отчет от {now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=json)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, charity_projects: list, wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]
    for res in charity_projects:
        new_row = [
            str(res['name']),
            str(res['collecting_time']),
            str(res['description']),
        ]
        table_values.append(new_row)

    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:C30',
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
