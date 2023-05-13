from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags for properties'
    
    name = fields.Char(required=True)
