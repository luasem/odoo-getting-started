from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    # Calcular una fecha futura
    three_months_from_now = fields.Date.today() + relativedelta(months=3)

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=three_months_from_now, string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Recieved'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default='new',
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        if self.garden is False:
            self.garden_area = 0
            self.garden_orientation = ''

    def sell_property(self):
        for record in self:
            if record.status == 'canceled':
                raise exceptions.UserError_('Canceled properties cannot be sold.')
            record.status = 'sold'
        return True

    def cancel_property(self):
        for record in self:
            if record.status == 'sold':
                raise exceptions.UserError_('Sold properties cannot be canceled.')
            record.status = 'canceled'
        return True

    # @api.ondelete(at_uninstall=False)
    # def _unlink_if_status_is_new_or_canceled(self):
    #     for property in self:
    #         if property.status not in ['new', 'canceled']:
    #             raise exceptions.UserError("Only new and canceled properties can be deleted!")
