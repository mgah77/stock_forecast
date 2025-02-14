from odoo import models, fields, api
from datetime import datetime, timedelta

class ProductProduct(models.Model):
    _inherit = 'product.product'

    average_monthly_sale = fields.Float(string='Promedio de Venta Mensual', compute='_compute_average_monthly_sale', store=True)
    estimated_exhaustion_month = fields.Date(string='Mes Aproximado de Agotamiento', compute='_compute_estimated_exhaustion_month', store=True)
    estimated_exhaustion_month_display = fields.Char(string='Mes de Agotamiento (Formato)', compute='_compute_estimated_exhaustion_month_display', store=True)

    @api.depends('stock_move_ids')
    def _compute_average_monthly_sale(self):
        for product in self:
            moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '>=', fields.Date.today() - timedelta(days=365))
            ])
            total_sold = sum(moves.mapped('product_uom_qty'))
            product.average_monthly_sale = total_sold / 12

    @api.depends('qty_available', 'average_monthly_sale')
    def _compute_estimated_exhaustion_month(self):
        for product in self:
            if product.qty_available > 0 and product.average_monthly_sale > 0:
                months_left = product.qty_available / product.average_monthly_sale
                estimated_date = datetime.now() + timedelta(days=months_left * 30)
                product.estimated_exhaustion_month = estimated_date.date()
            else:
                product.estimated_exhaustion_month = False

    @api.depends('estimated_exhaustion_month')
    def _compute_estimated_exhaustion_month_display(self):
        for product in self:
            if product.estimated_exhaustion_month:
                product.estimated_exhaustion_month_display = product.estimated_exhaustion_month.strftime('%B %Y')
            else:
                product.estimated_exhaustion_month_display = 'N/A'