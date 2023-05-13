from odoo import models, fields

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
