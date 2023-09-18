# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = '房屋报价'

    price = fields.Float(string='价格')
    status = fields.Selection([('accepted', '已接受'), ('refused', '已拒绝')], string='状态')
    partner_id = fields.Many2one('res.partner', string='客户')
    property_id = fields.Many2one('estate.property')
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')    # 依赖于假期时长
    def _compute_date_deadline(self):
        """自动获取到有效日期到什么时候"""
        for obj in self:
            obj.date_deadline = fields.Date.today() + relativedelta(days=obj.validity)

    def _inverse_date_deadline(self):
        """反函数，通过设置有效日期来自动计算出假期时长"""
        for obj in self:
            obj.validity = (obj.date_deadline - fields.Date.today()).days
