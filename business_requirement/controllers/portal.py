# Copyright 2019 Tecnativa - Alexandre Díaz
from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.addons.portal.controllers.portal import (
    CustomerPortal,
    pager as portal_pager, get_records_pager)


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        br_count = request.env['business.requirement'].search_count(
            self._prepare_br_base_domain())
        values.update({
            'business_requirement_count': br_count,
        })
        return values

    def _prepare_br_base_domain(self):
        partner = request.env.user.partner_id
        return [
            ('message_partner_ids', 'child_of', [
                partner.commercial_partner_id.id]),
            ('portal_published', '=', True)
        ]

    def _br_get_page_view_values(self, br, access_token, **kwargs):
        values = {
            'business_requirement': br,
            'page_name': 'business_requirement',
        }
        if access_token:
            values['no_breadcrumbs'] = True
            values['access_token'] = access_token
        values['portal_confirmation'] = br.get_portal_confirmation_action()

        if kwargs.get('error'):
            values['error'] = kwargs['error']
        if kwargs.get('warning'):
            values['warning'] = kwargs['warning']
        if kwargs.get('success'):
            values['success'] = kwargs['success']

        history = request.session.get('my_br_history', [])
        values.update(get_records_pager(history, br))

        return values

    @http.route(['/my/business_requirements',
                 '/my/business_requirements/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_br(self, page=1, date_begin=None, date_end=None,
                     sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        BRObj = request.env['business.requirement']

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'date desc'},
            'sequence': {'label': _('Sequence'), 'order': 'sequence'},
        }
        # default sortby br
        if not sortby:
            sortby = 'sequence'
        sort_br = searchbar_sortings[sortby]['order']

        domain = self._prepare_br_base_domain()

        archive_groups = self._get_archive_groups('business.requirement',
                                                  domain)
        if date_begin and date_end:
            domain += [('date', '>', date_begin),
                       ('date', '<=', date_end)]

        # count for pager
        br_count = BRObj.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/business_requirements",
            url_args={'date_begin': date_begin,
                      'date_end': date_end,
                      'sortby': sortby},
            total=br_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        business_requirements = BRObj.search(domain, order=sort_br,
                                             limit=self._items_per_page,
                                             offset=pager['offset'])
        request.session['my_br_history'] = business_requirements.ids[:100]

        values.update({
            'date': date_begin,
            'business_requirements': business_requirements.sudo(),
            'page_name': 'business_requirement',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/business_requirements',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("business_requirement.portal_my_br", values)

    @http.route(['/my/business_requirement/<int:br_id>'],
                type='http', auth="public", website=True)
    def portal_br_page(self, br_id=None, access_token=None, **kw):
        try:
            br_sudo = self._document_check_access(
                'business.requirement', br_id, access_token=access_token)
        except AccessError:
            return request.redirect('/my')

        values = self._br_get_page_view_values(br_sudo, access_token, **kw)
        return request.render("business_requirement.portal_br_page", values)

    def _get_br_report_name(self):
        return ('business_requirement.'
                'business_requirement_report')

    @http.route(['/my/business_requirement/pdf/<int:br_id>'],
                type='http', auth="public", website=True)
    def portal_br_report(self, br_id, access_token=None, **kw):
        try:
            br_sudo = self._document_check_access(
                'business.requirement', br_id, access_token=access_token)
        except AccessError:
            return request.redirect('/my')

        # print report as sudo
        pdf = request.env.ref(self._get_br_report_name())\
            .sudo().render_qweb_pdf([br_sudo.id])[0]
        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
