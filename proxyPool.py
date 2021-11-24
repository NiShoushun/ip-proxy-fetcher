# -*- coding: utf-8 -*-


import click

from core.launcher import startServer, startScheduler

import pyfiglet as title

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

VERSION = 1.0



@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def cli():
    """ProxyPool cli工具"""


@cli.command(name="schedule")
def schedule():
    """ 启动调度程序 """
    title.print_figlet(font='big', text='IP  PROXY  POOL', width=100000)
    startScheduler()


@cli.command(name="server")
def server():
    """ 启动api服务 """
    title.print_figlet(font='big', text='IP  PROXY  POOL  SERVER', width=100000)
    startServer()


if __name__ == '__main__':
    cli()
