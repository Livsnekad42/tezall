from typing import Dict, List, Union
from datetime import date
import json
import re


def json2interface(name: str, data: Dict) -> str:
    """
    Функция помогает быстро формировать интерфейсы TypeScript на основании Dict
    """
    data_pattern = re.compile(r"\d{2}\.\d{2}\.(\d{2}|\d{4}).*")
    if not isinstance(data, Dict):
        raise Exception("Для формирвания TypeScript интерфейса передайте Словарь")
    name = name.replace("List", "")
    name_interface = f'{name[0].title()}{name[1:]}'

    template = f'export interface {name_interface} ' + '{\n'
    for key in data:
        if isinstance(data[key], int):
            _type = "number"

        elif data_pattern.match(data[key]):
            _type = "Date"

        else:
            _type = "string"

        line = f'   {key}?: {_type}\n'
        template += line

    template += '}\n'

    return template


def main():
    js_list: List[Dict[str, str]] = [
        {
            "name_interface": "pawnTicketList",
            "content": '''{
                "id": 123456,
                "issueDate": "01.01.2020",
                "returnDate": "21.04.2020",
                "guaranteeDate": "01.06.2020",
                "creditSum": 100000,
                "lastPaymentDate": "05.03.2020",
                "creditPeriod": 80,
                "saldoSum": 100000,
                "interestSum": 0,
                "penaltySum": 50000,
                "totalSum": 150000,
                "totalSumOnReturnDate": 150000,
                "status": "Гарантийный срок"
              }'''
        },
        {
            "name_interface": "pawnTicketOperations",
            "content": '''{
                "operDate": "05.03.2020 12:32:49",
                "operType": "Оплата % за кредит",
                "operSum": 10000,
                "operPlace": "Отделение №1"
              }
            '''
        },
        {
            "name_interface": "pawnPropertyList",
            "content": '''{
                "propertyId": 98768,
                "positionNumber": 2,
                "name": "Ювелирные изделия"
              }
            '''
        },
        {
            "name_interface": "pawnProperties",
            "content": '''
            {
                "positionNumber": 1,
                "name": "Техника",
                "description": "Сотовый телефон Samsung D600 в коробке в комплекте зарядка + наушники IMEI 345671127777789"
              }
            '''
        }
    ]

    with open("model.ts", 'w') as f:
        for js_data in js_list:
            data = json.loads(js_data["content"])
            template_interface = json2interface(js_data["name_interface"], data)
            template_interface += "\n\n"
            f.write(template_interface)
            f.flush()


if __name__ == "__main__":
    main()
