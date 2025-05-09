from odoo import models, fields, api
from datetime import datetime, timedelta

class ProductProduct(models.Model):
    _inherit = 'product.product'

    average_monthly_sale = fields.Float(string='Promedio de Venta Mensual', compute='_compute_average_monthly_sale', store=True)
    estimated_exhaustion_month = fields.Char(string='Mes Aproximado de Agotamiento', compute='_compute_estimated_exhaustion_month', store=True)
    estimated_month = fields.Date(string='Mes', compute='_compute_estimated_exhaustion_month', store=True)

    @api.depends('stock_move_ids')
    def _compute_average_monthly_sale(self):
        for product in self:
            moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '>=', fields.Date.today() - timedelta(days=183))
            ])
            total_sold = sum(moves.mapped('product_uom_qty'))
            product.average_monthly_sale = total_sold / 6

    @api.depends('qty_available', 'average_monthly_sale')
    def _compute_estimated_exhaustion_month(self):
        for product in self:
            if product.qty_available > 0 and product.average_monthly_sale > 0:
                months_left = product.qty_available / product.average_monthly_sale
                estimated_date = datetime.now() + timedelta(days=months_left * 30)
                product.estimated_month = estimated_date.replace(day=1).date()
                product.estimated_exhaustion_month = estimated_date.strftime('%B %Y')
            else:
                product.estimated_exhaustion_month = 'N/A'