from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'
    
    def action_sell_property(self):
        for record in self:
            partner_id = record.buyer_id
            move_type = 'out_invoice'
            # journal = self.env['account.journal'].create({
            #     'name': 'First Journal',
            #     'code': 'code',
            #     'type': 'sale',
                
            # })
            journal_id = 1
            account_move = self.env['account.move'].create({
                'partner_id': partner_id.id,
                'move_type': move_type,
                'journal_id': journal_id,
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Inline move',
                        'quantity': 1.0,
                        'price_unit': 150000.0
                    }),
                ],
            })
        return super().action_sell_property()
