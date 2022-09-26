from odoo import models


class Property(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        return super()
