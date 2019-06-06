
from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.http import request
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers.portal import (
    CustomerPortal,
    pager as portal_pager, get_records_pager)
from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):

    def _get_br_report_name(self):
        return ('business_requirement_deliverable.'
                'business_requirement_deliverable')

    @http.route(['/my/brd', '/my/brd/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_brd(self, page=1, date_begin=None, date_end=None,
                      sortby=None, filterby=None, search=None,
                      search_in='content', groupby='business_requirement',
                      **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Title'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
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
            'state': {'input': 'state', 'label': _('Search in States')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'business_requirement': {'input': 'br',
                                     'label': _('Business Requirement')},
        }

        # extends filterby criteria with br the customer has access to
        business_requirements = request.env['business.requirement'].search([])
        for br in business_requirements:
            searchbar_filters.update({
                str(br.id): {
                    'label': br.name,
                    'domain': [('business_requirement_id', '=', br.id)]
                }
            })

        BRDObj = request.env['business.requirement.deliverable']

        # extends filterby criteria with br (criteria name is the br id)
        # Note: portal users can't view brd they don't follow
        brd_groups = BRDObj.read_group(
                [('business_requirement_id', 'not in',
                  business_requirements.ids)],
                ['business_requirement_id'],
                ['business_requirement_id']
            )
        for group in brd_groups:
            br_id = group['business_requirement_id'][0] \
                if group['business_requirement_id'] else False
            br_name = group['business_requirement_id'][1] \
                if group['business_requirement_id'] else _('Others')
            searchbar_filters.update({
                str(br_id): {
                    'label': br_name,
                    'domain': [('business_requirement_id', '=', br_id)]
                }
            })

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        # archive groups - Default Group By 'create_date'
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
                                    [('partner_id', 'ilike', search)]])
            if search_in in ('message', 'all'):
                search_domain = OR([search_domain,
                                    [('message_ids.body', 'ilike', search)]])
            if search_in in ('state', 'all'):
                search_domain = OR([search_domain,
                                    [('state', 'ilike', search)]])
            domain += search_domain

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
        brd_recs = BRDObj.search(domain, order=order,
                                 limit=self._items_per_page,
                                 offset=(page - 1) * self._items_per_page)
        request.session['my_brd_history'] = brd_recs.ids[:100]
        if groupby == 'business_requirement':
            grouped_brd = [
                BRDObj.concat(*g) for k, g in groupbyelem(
                    brd_recs, itemgetter('business_requirement_id'))]
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

    @http.route(['/my/brd/<int:brd_id>'],
                type='http', auth="user", website=True)
    def portal_my_task(self, brd_id=None, **kw):
        brd = request.env['business.requirement.deliverable'].browse(brd_id)
        brd.check_access_rights('read')
        brd.check_access_rule('read')

        vals = {
            'brd': brd,
            'user': request.env.user
        }
        history = request.session.get('my_brd_history', [])
        vals.update(get_records_pager(history, brd))
        return request.render("business_requirement_deliverable.portal_my_brd",
                              vals)
