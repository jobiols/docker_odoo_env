# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import yaml
import json
import argparse
from docker_odoo_env.__init__ import __version__
from docker_odoo_env.messages import Msg

msg = Msg()

user_config_path = os.path.expanduser('~') + '/.config/oe/'
user_config_file = user_config_path + 'config.yaml'


def merge_args(args, config):
    """
    A los datos que estan en args les agrega los datos que vienen en config

    :param args: (namespace) argumentos del parser
    :param config: (dictionary) argumentos del config.yml
    :return: args + config (dictionary)
    """
    # convertir args a dict
    ret = vars(args)

    # agregar el default para database
    if not ret['database'] and ret['client']:
        ret['database'] = ret['client'] + '_prod'

    # si hay algo en config pasarlo a ret si en ret no hay nada
    if config:
        for item in ret:
            if not ret[item]:
                ret[item] = config.get(item, None)

    return ret


def command_config(data):
    msg.run('Saved options')
    for item in data:
        msg.inf('{:11} -> {}'.format(item, str(data.get(item))))


def command_update(args, data):
    if args.debug:
        data['debug'] = args.debug
    if args.client:
        data['client'] = args.client
    return data


def save_config(data):
    if not os.path.exists(user_config_path):
        os.makedirs(user_config_path)
    with open(user_config_file, 'w') as config:
        yaml.dump(data, config, default_flow_style=False, allow_unicode=True)


def get_config():
    try:
        with open(user_config_file, 'r') as config:
            ret = yaml.safe_load(config)
    except Exception:
        return False
    return ret


def new_config_parser(sub):
    parser = sub.add_parser('config',
                            help='config current configuration')
    parser.add_argument('-c', '--client',
                        dest='client',
                        help='Client name')
    parser.add_argument('-e',
                        dest='environment',
                        choices=['production', 'staging', 'development'],
                        default='production',
                        help='Environment where to deploy')
    parser.add_argument('-n', '--nginx',
                        dest='nginx',
                        default='on',
                        choices=['on', 'off'],
                        help='Install Nginx reverse proxy')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        default='off',
                        choices=['on', 'off'],
                        help='Install Nginx reverse proxy')
    parser.add_argument('-d', '--database',
                        dest='database',
                        help='Default database')
    parser.add_argument('--defapp',
                        dest='defapp',
                        help='git path for default main application')


def new_update_parser(sub):
    parser = sub.add_parser('update',
                            help='creates or updates an installation')
    parser.add_argument('-d',
                        dest='debug',
                        choices=['on', 'off'],
                        help='force restart and change debug mode')
    parser.add_argument('-c',
                        dest='client',
                        help='Client code')
    parser.add_argument('-r',
                        help='Restart server')


def new_backup_parser(sub):
    parser = sub.add_parser('backup',
                            help='generates a backup in the backup_dir '
                                 'folder')


def new_up_parser(sub):
    parser = sub.add_parser('up',
                            help='Start docker images')


def new_down_parser(sub):
    parser = sub.add_parser('down',
                            help='Stop docker images')


def new_restore_parser(sub):
    parser = sub.add_parser('restore',
                            help='restores a database from backup_dir')


def new_qa_parser(sub):
    parser = sub.add_parser('qa',
                            help='quality analisys')
    parser.add_argument('-d',
                        dest='test_database',
                        help='test database name')


def parse():
    """ parsear los argumentos y completarlos con los datos almacenados en la
        configuracion devuelve un diccionario con los parametros
    """

    parser = argparse.ArgumentParser(description="""
==============================================================================
Odoo Environment {} - by jeo Software <jorge.obiols@gmail.com>
==============================================================================
""".format(__version__))

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument('-H',
                        dest='help',
                        help='odoo server server help')

    subparser = parser.add_subparsers(help='commands', dest='command')
    new_config_parser(subparser)
    new_update_parser(subparser)
    new_up_parser(subparser)
    new_down_parser(subparser)
    new_backup_parser(subparser)
    new_restore_parser(subparser)
    new_qa_parser(subparser)

    # obtengo los comandos del runstring
    args = parser.parse_args()

    # le agrego los comandos almacenados
    data = merge_args(args, get_config())
    save_config(data)

    if args.command:
        if args.command == 'config':
            return command_config(data)

        if args.command == 'update':
            return command_update(args, data)

    if args.command:
        data['command'] = args.command
