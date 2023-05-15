from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Tags for properties'
    _order = 'name'
    
    name = fields.Char(required=True)
    color = fields.Integer()
    
    _sql_constraints = [
        # (name, sql_definition, message)
        ('check_name_unique', 'unique (name)',
         'The property tag name must be unique'),
    ]
