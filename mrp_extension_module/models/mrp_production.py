from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    forced_back_date = fields.Datetime(
        string='Forced Backdate',
        help="If set, this date will be used for stock moves instead of the current date."
    )

    @api.onchange('forced_back_date')
    def _onchange_forced_back_date(self):
        if self.forced_back_date:
            self.date_finished = self.forced_back_date

    @api.model
    def _get_default_date_finished(self):
        if self.env.context.get('default_forced_back_date'):
            return fields.Datetime.to_datetime(
                self.env.context.get('default_forced_back_date')
            )
        return super()._get_default_date_finished()

    def _redate_account_moves(self, account_moves, backdate):
        """
        Safely redate posted journal entries to backdate.
        Handles the sequence name mismatch that occurs when the new date
        falls in a different month/year than the original entry.
        """
        for move in account_moves.sudo():
            if move.state == 'posted':
                # Step 1: Reset the sequence name so Odoo re-assigns it
                # based on the new date. Without this, Odoo raises a
                # validation error when the date and sequence month mismatch.
                move.sudo().write({'name': '/'})

                # Step 2: Now safely write the new date. Odoo will assign
                # a new sequence number consistent with the backdate.
                move.sudo().write({'date': backdate})

            elif move.state == 'draft':
                # Draft entries have no locked sequence, safe to just redate
                move.sudo().write({'date': backdate})

    def button_mark_done(self):
        res = super().button_mark_done()

        for production in self.filtered(
            lambda p: p.forced_back_date and p.state == 'done'
        ):
            backdate = production.forced_back_date

            # 1. Fix the production date itself
            production.write({'date_finished': backdate})

            # 2. Fix finished and raw stock moves
            all_done_moves = (
                production.move_finished_ids | production.move_raw_ids
            ).filtered(lambda m: m.state == 'done')
            all_done_moves.write({'date': backdate})

            # 3. Fix move lines
            all_done_moves.move_line_ids.write({'date': backdate})

            # 4. Fix valuation layer create_date via SQL
            layers = all_done_moves.sudo().stock_valuation_layer_ids
            if layers:
                self.env.cr.execute(
                    """
                    UPDATE stock_valuation_layer
                    SET create_date = %s
                    WHERE id = ANY(%s)
                    """,
                    (backdate, layers.ids)
                )
                layers.invalidate_recordset(['create_date'])

            # 5. Fix journal entries with safe sequence reset
            account_moves = layers.account_move_id
            if account_moves:
                # Guard against fiscally locked periods
                lock_date = production.company_id.fiscalyear_lock_date
                valid_moves = account_moves.sudo().filtered(
                    lambda am: not lock_date
                    or backdate.date() > lock_date
                )
                if valid_moves:
                    self._redate_account_moves(valid_moves, backdate)

        return res




