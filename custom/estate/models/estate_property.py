from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperties(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Advertising properties table'

    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
        help="Garden Orientation shows in which direction is the garden oriented")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    buyer_id = fields.Many2one('res.partner', copy=False, string='Buyer')
    salesperson_id = fields.Many2one(
        'res.users', default=lambda self: self.env.user, string='Salesman')

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Integer(
        string='Total Area (sqm)', compute='_compute_area')

    best_price = fields.Float(compute='_best_price', string='Best Offer')
    
    # sql Constraints
    _sql_constraints = [
        # (name, sql_definition, message)
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'A property selling price must be positive'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _best_price(self):
        for record in self:
            try:
                record.best_price = max(self.mapped('offer_ids.price'))
            except Exception:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
            return {'warning': {
                'title': _("Warning"),
                'message': ('North set as garden orientation, change if needed')}}
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sell_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold")
            elif record.state == 'sold':
                raise UserError('Property already sold')
            else:
                record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Property already canceled")
            elif record.state == 'sold':
                raise UserError('Sold properties cannot be canceled')
            else:
                record.state = 'canceled'
        return True
    
    @api.constrains('selling_price')
    def _check_price_not_too_lower(self):
        for record in self:
            if not float_is_zero(record.selling_price, 3) :
                if record.selling_price < record.expected_price * 0.9:
                    raise ValidationError("The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer")
