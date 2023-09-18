# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = '房屋信息数据'

    name = fields.Char(string='名称', default='Unknown')  # 当该字段没填时默认为'Unknown'
    description = fields.Text(string='描述')
    postcode = fields.Char(string='邮编')
    date_availability = fields.Date(string='到期时间')  # xxx年xx月xx日
    expected_price = fields.Float(string='期望价格')
    selling_price = fields.Float(string='销售价格')
    bedrooms = fields.Integer(string='房间数量')
    living_area = fields.Integer(string='居住面积')
    facades = fields.Selection([('North', '北'),
                                ('South', '南'),
                                ('East', '东'),
                                ('West', '西')],
                               string='朝向')
    garage = fields.Boolean(string='是否带车库')
    garden = fields.Boolean(string='是否带花园')
    garage_area = fields.Integer(string='车库面积')
    garden_area = fields.Integer(string='花园面积')
    garage_orientation = fields.Selection([('North', '北'),
                                           ('South', '南'),
                                           ('East', '东'),
                                           ('West', '西')],
                                          string='车库朝向')
    garden_orientation = fields.Selection([('North', '北'),
                                           ('South', '南'),
                                           ('East', '东'),
                                           ('West', '西')],
                                          string='花园朝向')
    # 枚举类型字段，元组中的第一个值为数据库中的存储值，第二值为实际显示值

    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    # 获取到当前创建这条记录的时间

    saleman_id = fields.Many2one('res.users', string='卖家')  # 一个卖家可以有多个房产交易
    buyer_id = fields.Many2one('res.partner', string='买家')  # 一个买家可以有多个房产交易
    property_type_id = fields.Many2one('estate.property.type', string='房屋类型')
    # 同一种房屋类型可能有多笔房产交易

    tag_ids = fields.Many2many('estate.property.tag',
                               'estate_property_estate_property_tag_rel',
                               'property_id',
                               'tag_id',
                               string='标签')
    # （Many2many关联的模型，中间表的名称，中间表第一个字段的名称，中间表第二个字段的名称，标签的名称）
    # 一个房产交易可有多个标签，一个类型的标签可以存在多个房产交易之中

    test_float = fields.Float(string='测试浮点型字段')
    test_int = fields.Integer(string='测试整型字段')
    #  测试字段

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='报价 ')
    # (One2many关联的模型，One2many对应的Many2one名称,标签的名称)
    # 一个房产交易可以有多个报价

    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')
    total_area = fields.Integer(string='Total Area', compute='_compute_total_area')

    @api.depends('living_area', 'garden_area', 'garage_area')  # 依赖于居住面积,花园面积和车库面积
    def _compute_total_area(self):
        """自动计算房屋的总面积，居住面积加花园面积加车库面积"""
        for obj in self:
            obj.total_area = obj.living_area + obj.garden_area + obj.garage_area

    @api.depends('offer_ids.price')  # 依赖于offer里面的价格
    def _compute_best_price(self):
        """自动计算总的最佳价格"""
        for obj in self:
            best_price = 0.0
            for line in obj.offer_ids:
                best_price += line.price
            obj.best_price = best_price

    @api.onchange('garden')  # 依赖于是否有花园
    def onchange_garden(self):
        """有花园默认给朝向为北，花园面积为50，没有花园则为空和0"""
        if self.garden:
            self.garden_orientation = 'North'
            self.garden_area = 50
        else:
            self.garden_orientation = None
            self.garden_area = 0

    @api.onchange('garage')  # 依赖于是否有车库
    def onchange_garage(self):
        """有车库默认给朝向为南，车库面积为20，没有车库则为空和0"""
        if self.garage:
            self.garage_orientation = 'South'
            self.garage_area = 20
        else:
            self.garage_orientation = None
            self.garage_area = 0
