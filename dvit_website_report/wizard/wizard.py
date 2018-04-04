# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo import models, fields, api

class dvitwebsiteReport(models.Model):
    _name = "dvit.website.report"
    _description = "Website Report"

    date_from = fields.Date(string='Start Date')
    date_to = fields.Datetime(string='End Date')
    sale_lines_ids = fields.One2many(comodel_name="sale.order.report", inverse_name="order_id", string="Order Lines")

    @api.multi
    def pre_print_report(self):

        sale_order_report_model = self.env['sale.order.report'].search([])
        sale_order_report_model.unlink()
        if (self.date_from <= self.date_to):
            quotation_new = self.env['sale.order'].search([('date_order', '>=', self.date_from),
                                                           ('date_order', '<=', self.date_to)])
            partner_id_current = 0
            amount_total_old = 0
            last_id = 0
            vals = {}
            for i in quotation_new:
                order_line = self.env['sale.order.line'].search([('order_partner_id', '=', i.partner_id.id)])
                print "---------------------------------------------",  i.date_order

                if last_id != i.id:
                    partner_id_current = 0
                    amount_total_old = 0


                for j in order_line:
                    if partner_id_current == i.partner_id:
                        partner_id_current = '0'
                    else:
                        partner_id_current = i.partner_id

                    if amount_total_old == i.amount_total:
                        amount_total_old = '0'
                    else:
                        amount_total_old = i.amount_total

                    vals = {
                        'customer_id': partner_id_current,
                        'order_id': i.id,
                        'pro_name': j.product_id.name,
                        'pro_type': j.product_id.type,
                        'pro_uom_qty': j.product_uom_qty,
                        'pro_price_unit': j.price_unit,
                        'total': amount_total_old,
                    }
                    self.sale_lines_ids.create(vals)
                    print ">>>>>>>>>>>>>>>>>>>>>>>>", j.product_id.name
                    amount_total_old = i.amount_total
                    partner_id_current = i.partner_id

                if last_id != i.id:
                    last_id = i.id


            return self.env['report'].get_action(docids=sale_order_report_model,
                                                 report_name='dvit_website_report.report_saleorder_document_inherit_document')

        else:
            raise ValidationError(_("not valid..! ( End Date ) must be bigger than ( Start Date ) "))

class sale_order_report(models.Model):
    _name = "sale.order.report"
    _description = "Sale Order Report"

    order_id = fields.Many2one(comodel_name="dvit.website.report", string="order id")
    customer_id = fields.Char("Customer Name")
    pro_name = fields.Char("name")
    pro_type = fields.Char("type")
    pro_uom_qty = fields.Float("Qty")
    pro_price_unit = fields.Float("price")
    total = fields.Float()

