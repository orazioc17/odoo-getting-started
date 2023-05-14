from odoo import models, fields

class EstatePropertyTypes(models.Model):
    _name = 'estate.property.type'
    _description = 'Type of the property'
    
    name = fields.Char(required=True)
    
    _sql_constraints = [
        # (name, sql_definition, message)
        ('check_name_unique', 'unique (name)',
         'The property type name must be unique'),
    ]
