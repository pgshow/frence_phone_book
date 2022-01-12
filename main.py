import re
import time
import fc
import click
from scrape import Scrape
from loguru import logger


@click.command()
@click.option('--link', default="", help='The list page link.')
@click.option('--name', default="", help='Human name.')
@click.option('--location', default="", help='The location.')
def run(link, name, location):
    if link:
        tmp = re.search(r'quoiqui=(.+?)&ou=(.+?)&univers.+?&idOu=([0-9A-Z]+)', link)
        if not tmp or len(tmp.groups()) != 3:
            logger.error('Link is illegal, must include Name, Location and idOu')
            exit(-1)

        name = fc.str_filter(tmp.group(1))
        location = fc.str_filter(tmp.group(2))
        idOu = tmp.group(3)
    else:
        if not location:
            logger.error('Location can not be empty')
            exit(-1)

    scrape_obj = Scrape(name, location, idOu)
    scrape_obj.run()


if __name__ == '__main__':
    run()
