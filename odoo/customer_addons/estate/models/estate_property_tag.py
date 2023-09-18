# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = '房屋标签'

    name = fields.Char(string='名称')
