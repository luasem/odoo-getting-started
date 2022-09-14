from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse='_inverse_deadline')

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            create_date = fields.Date.today()
            if record.create_date:
                create_date = record.create_date
            record.date_deadline = create_date + relativedelta(days=int(record.validity))

    def _inverse_deadline(self):
        for record in self:
            fmt = "%Y-%m-%d"
            create_date = fields.Date.today()
            if record.create_date:
                create_date = record.create_date
            d1 = datetime.strptime(fields.Date.to_string(fields.Date.to_date(create_date)), fmt)
            d2 = datetime.strptime(fields.Date.to_string(record.date_deadline), fmt)
            record.validity = (d2 - d1).days
