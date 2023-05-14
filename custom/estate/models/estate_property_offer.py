from odoo import models, fields, api
from dateutil import relativedelta
from datetime import datetime

class EstatePropertyOffers(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers for properties'
    
    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one ('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    
    validity = fields.Integer(default=7, string='Validity')
    date_deadline = fields.Date(compute='_date_with_validity', inverse='_inverse_date_validity', readonly=False)
    
    @api.depends('validity', 'create_date')
    def _date_with_validity(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = datetime.now() + relativedelta.relativedelta(days=record.validity)
            else:
                record.date_deadline = record.create_date + relativedelta.relativedelta(days=record.validity)
        
    def _inverse_date_validity(self):
        for record in self:
            days = (record.date_deadline - record.create_date.date()).days
            if record.validity != days:
                record.validity = days
