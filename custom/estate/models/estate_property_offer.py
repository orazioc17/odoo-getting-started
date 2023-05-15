from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from dateutil import relativedelta
from datetime import datetime

class EstatePropertyOffers(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers for properties'
    _order = 'price desc'
    
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
    
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id')
        
    _sql_constraints = [
        # (name, sql_definition, message)
        ('check_offer_price', 'CHECK(price >= 0)',
         'An offer price must be strictly positive'),
    ]
    
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
            
    def action_accept(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError('The offer have been already accepted')
            elif record.property_id.selling_price > 0:
                raise UserError('An offer have been already accepted')
            else:
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.status = 'accepted'
                
        return True
    
    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError('The offer have been already accepted')
            else:
                record.status = 'refused'
                
        return True

    @api.model
    def create(self, vals):
        estate_property = self.env['estate.property'].browse(vals['property_id'])

        if len(estate_property.mapped('offer_ids.price')) > 0:
            offers = list(estate_property.mapped('offer_ids.price'))
            offers.sort()
            if vals['price'] < offers[-1]: # Comparando la oferta actual con la oferta de mayor precio
                raise ValidationError(f'The offer must be higher than {offers[-1]}.')
        else:
            estate_property.state = 'offer_received'
        return super().create(vals)
