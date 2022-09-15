from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many('estate.property', 'property_type_id')

    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'The name must be unique.')]
