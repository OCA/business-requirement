# Copyright 2019 Tecnativa - Alexandre Díaz
from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.http import request
from odoo.tools import groupby as groupbyelem
from odoo.exceptions import AccessError
from odoo.addons.portal.controllers.portal import (
    CustomerPortal,
    pager as portal_pager,
    get_records_pager)
from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        dl_count = request.env[
            'business.requirement.deliverable'
        ].search_count(self._prepare_br_base_domain())
        values.update({
            'dl_count': dl_count,
        })
        return values

    def _prepare_brd_base_domain(self, business_requirements):
        partner = request.env.user.partner_id
        return [
            ('message_partner_ids', 'child_of', [
                partner.commercial_partner_id.id]),
            ('portal_published', '=', True),
            ('business_requirement_id', 'in', business_requirements.ids)
        ]

    @http.route(['/my/brd', '/my/brd/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_brd_list(self, page=1, date_begin=None, date_end=None,
                           sortby=None, filterby=None, search=None,
                           search_in='content', groupby='section',
                           **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Title'), 'order': 'name'},
            'ref': {'label': _('Reference'), 'order': 'sequence'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        searchbar_inputs = {
            'content': {
                'input': 'content',
                'label': _('Search <span class="nolabel"> (in Content)</span>')
            },
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'stakeholder': {'input': 'stakeholder',
                            'label': _('Search in Stakeholder')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'business_requirement': {'input': 'br',
                                     'label': _('Business Requirement')},
            'section': {'input': 'section',
                        'label': _('Section')},
        }

        # extends filterby criteria with br the customer has access to
        business_requirements = request.env['business.requirement'].search(
            self._prepare_br_base_domain())
        domain = self._prepare_brd_base_domain(business_requirements)
        for br in business_requirements:
            searchbar_filters.update({
                str(br.id): {
                    'label': br.name,
                    'domain': [('business_requirement_id', '=', br.id)]
                }
            })

        # default sort by value
        if not sortby:
            sortby = 'ref'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # archive groups - Default Group By 'sequence'
        archive_groups = self._get_archive_groups(
            'business.requirement.deliverable', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain,
                                    [('name', 'ilike', search)]])
            if search_in in ('stakeholder', 'all'):
                search_domain = OR([search_domain,
                                    [('business_requirement_id.partner_id',
                                      'ilike', search)]])
            if search_in in ('message', 'all'):
                search_domain = OR([search_domain,
                                    [('message_ids.body', 'ilike', search)]])
            domain += search_domain

        BRDObj = request.env['business.requirement.deliverable']

        # brd count
        brd_count = BRDObj.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/brd",
            url_args={
                'date_begin': date_begin, 'date_end': date_end,
                'sortby': sortby, 'filterby': filterby,
                'search_in': search_in, 'search': search},
            total=brd_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        if groupby == 'business_requirement':
            # Force sort on br first to group by br in view
            order = "business_requirement_id, %s" % order
        elif groupby == 'section':
            order = "section_id, %s" % order
        brd_recs = BRDObj.search(domain, order=order,
                                 limit=self._items_per_page,
                                 offset=(page - 1) * self._items_per_page)
        request.session['my_brd_history'] = brd_recs.ids[:100]
        if groupby == 'business_requirement':
            grouped_brd = [
                BRDObj.concat(*g) for k, g in groupbyelem(
                    brd_recs, itemgetter('business_requirement_id'))]
        elif groupby == 'section':
            grouped_brd = [
                BRDObj.concat(*g) for k, g in groupbyelem(
                    brd_recs, itemgetter('section_id'))]
        else:
            grouped_brd = [brd_recs]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_brd': grouped_brd,
            'page_name': 'business_requirement_deliverable',
            'archive_groups': archive_groups,
            'default_url': '/my/brd',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(
                sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render(
            "business_requirement_deliverable.portal_my_brd_list", values)

    def _brd_get_page_view_values(self, brd, access_token, **kwargs):
        values = {
            'brd': brd,
            'page_name': 'business_requirement_deliverable',
            'user': request.env.user,
        }
        if access_token:
            values['no_breadcrumbs'] = True
            values['access_token'] = access_token

        if kwargs.get('error'):
            values['error'] = kwargs['error']
        if kwargs.get('warning'):
            values['warning'] = kwargs['warning']
        if kwargs.get('success'):
            values['success'] = kwargs['success']

        history = request.session.get('my_br_history', [])
        values.update(get_records_pager(history, brd))

        return values

    @http.route(['/my/brd/<int:brd_id>'],
                type='http', auth="user", website=True)
    def portal_my_brd(self, brd_id=None, access_token=None, **kw):
        try:
            brd_sudo = self._document_check_access(
                'business.requirement.deliverable', brd_id, access_token)
        except AccessError:
            return request.redirect('/my')

        if not brd_sudo.portal_published:
            raise AccessError(
                _("Can't access to this business requirement deliverable"))

        values = self._brd_get_page_view_values(brd_sudo, access_token, **kw)
        return request.render("business_requirement_deliverable.portal_my_brd",
                              values)

    def _br_get_page_view_values(self, br, access_token, **kwargs):
        vals = super(CustomerPortal, self)._br_get_page_view_values(
            br, access_token, **kwargs)

        BRDObj = request.env['business.requirement.deliverable']
        brd_count = BRDObj.search_count(
            self._prepare_brd_base_domain(br))
        vals.update({
            'brd_count': brd_count,
        })
        return vals
