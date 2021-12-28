import pandas
from datetime import datetime
from loguru import logger

import fc


def save_excel(data, name, location):
    """保存结果"""
    try:
        df = pandas.DataFrame(data, columns=["full name", "phone number", "address", "email"])

        df = df.set_index('full name')

        s = '_'.join([name, location, datetime.now().strftime('%m-%d %H-%M-%S')])

        path = f"./result/{s}.xlsx"

        df.to_excel(path)

        logger.success(f'Save to: {path}')
    except Exception as e:
        logger.error(e)