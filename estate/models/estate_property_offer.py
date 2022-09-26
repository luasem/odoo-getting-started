from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, exceptions, fields, models, tools


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse='_inverse_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [('positive_price', 'CHECK(price > 0)', 'The price offer must be strictly positive.')]

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

    def accept_offer(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise exceptions.UserError(_('This property has already been sold. Offers can no longer be accepted'))
            record.state = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    @api.constrains('state', 'property_id.expected_price')
    def _min_selling_price(self):
        for record in self:
            if record.state == 'accepted':
                if tools.float_compare(record.price, record.property_id.expected_price * 0.9, 2) == -1:
                    raise exceptions.ValidationError(
                        _(
                            "The selling price must be at least"
                            " 90% of the expected price! Try reducing"
                            " the expected price."
                        )
                    )

    def reject_offer(self):
        for record in self:
            record.state = 'refused'
        return True

    @api.model
    def create(self, vals):
        estate_property = self.env['estate.property'].browse(vals['property_id'])
        if any(offer.price > vals['price'] for offer in estate_property.offer_ids):
            raise exceptions.UserError(_('New offers can\'t be lower than existing ones!'))
        estate_property.set_offer_received()
        return super().create(vals)
