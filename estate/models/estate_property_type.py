from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'The name must be unique.')]
