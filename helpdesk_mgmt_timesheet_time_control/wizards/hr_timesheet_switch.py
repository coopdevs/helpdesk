# Copyright 2020 Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrTimesheetSwitch(models.TransientModel):
    _inherit = "hr.timesheet.switch"

    @api.model
    def _closest_suggestion(self):
        """Find most similar account.analytic.line for tickets or
        call super for other models."""
        if self.env.context.get("active_model") == "helpdesk.ticket":
            try:
                domain = [
                    ("user_id", "=", self.env.user.id),
                    ("ticket_id", "=", self.env.context["active_id"]),
                ]
            except KeyError:
                # If I don't know where's the user, I don't know what to suggest
                return self.env["account.analytic.line"].browse()
            return self.env["account.analytic.line"].search(
                domain, order="date_time DESC", limit=1,
            )
        else:
            return super()._closest_suggestion()
