from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags for properties'
    
    name = fields.Char(required=True)
    
    _sql_constraints = [
        # (name, sql_definition, message)
        ('check_name_unique', 'unique (name)',
         'The property tag name must be unique'),
    ]
