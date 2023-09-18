# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = '房屋类型'

    name = fields.Char(string='名称')
