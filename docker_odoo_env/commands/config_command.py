# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from docker_odoo_env.commands.command import Command


class ConfigCommand(Command):

    def execute(self):
        self._config.list()
