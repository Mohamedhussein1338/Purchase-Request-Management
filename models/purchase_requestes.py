from odoo import models, fields, api,_


class PurchaseRequestes(models.Model):
    _name = 'purchase.requestes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Request'


    name = fields.Char(string='Request Name', required=True)

    requested_by = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, required=True)

    start_date = fields.Date(string='Start Date', default=fields.Date.today())

    end_date = fields.Date(string='End Date')

    rejection_reason = fields.Text(string='Rejection Reason', invisible=True, readonly=True)

    orderlines = fields.One2many('purchase.request.line', 'purchase_request_id', string='Order Lines')

    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    status = fields.Selection([('draft', 'Draft'),('to_be_approved', 'To be Approved'),
                                ('approve', 'Approve'),('reject', 'Reject'),
                                ('cancel', 'Cancel'),], string='Status', default='draft')


    def action_submit_for_approval(self):
        self.status = 'to_be_approved'

    def action_cancel(self):
        self.status = 'cancel'

    def action_approve(self):
        group_purchase_manager = self.env.ref('purchase_request_module.group_manager_purchase_id')
        # Get all users in the purchase managers group
        manager_users = group_purchase_manager.users
        template = self.env.ref('purchase_request_module.email_template_purchase_approved')
        for user in manager_users:
            # Send email using the template
            template.send_mail(self.id, force_send=True, email_values={'email_to': user.email})
            print(f'Email sent for approval to : {user.name} - Your Email is: {user.email}')
            # Email sent for approval to: Marc Demo - Your Email is: mark.brown23@example.com
            # Email sent for approval to: Mohamed - Your Email is: proengmht@gmail.com
        # Update the status to "approve"
        self.status = "approve"

    def action_reset_to_draft(self):
        self.status = 'draft'


    def action_reject(self):
        return {
            'name': _('Rejection Reason'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'rejection.reason',
            'target': 'new',
        }

    @api.depends('orderlines.total')
    def _compute_total_price(self):
        for request in self:
            request.total_price = sum(request.orderlines.mapped('total'))

    # @api.model
    # def create(self, values):
    #     values['name'] = self.env["ir.sequence"].next_by_code("purchase.request")
    #     return super(PurchaseRequestes, self).create(values)
