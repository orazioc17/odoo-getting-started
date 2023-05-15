from odoo import models, fields, api

class EstatePropertyTypes(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of the property'
    _order = 'name'
    
    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')
    
    _sql_constraints = [
        # (name, sql_definition, message)
        ('check_name_unique', 'unique (name)',
         'The property type name must be unique'),
    ]
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            counter = 0
            for _ in record.mapped('offer_ids'):
                counter += 1
            record.offer_count = counter

