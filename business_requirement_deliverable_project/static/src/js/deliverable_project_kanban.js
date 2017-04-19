openerp.business_requirement_deliverable_project = function (instance) {
	
	var _t = instance.web._t,
	   _lt = instance.web._lt;
	var QWeb = instance.web.qweb;
	
	instance.web_kanban.KanbanView.include({
		set_domain: function(groups){
			var temp_app = false;
            var temp_draft = false;
            var temp_confirm = false;
            var temp_stakeholder_approval = false;
            var temp_in_progress = false;
            var temp_done = false;
            var temp_cancel = false;
            var temp_drop = false;
            _.each(groups,function(res){
                if(res.get('value') == 'approved'){
                    temp_app = res
                }
                if(res.get('value') == 'draft'){
                	temp_draft = res
                }
                if(res.get('value') == 'confirmed'){
                	temp_confirm = res
                }
                if(res.get('value') == "stakeholder_approval"){
                	temp_stakeholder_approval = res
                }
                if(res.get('value') == 'in_progress'){
                    temp_in_progress = res
                }
                if(res.get('value') == 'done'){
                	temp_done = res
                }
                if(res.get('value') == 'cancel'){
                	temp_cancel = res
                }
                if(res.get('value') == "drop"){
                	temp_drop = res
                }
            });
            groups = [];
            if(temp_draft){
            	groups.push(temp_draft);
            }
            if(temp_confirm){
            	groups.push(temp_confirm)
            }
            if(temp_app){
            	groups.push(temp_app)
            }
            if(temp_stakeholder_approval){
            	groups.push(temp_stakeholder_approval)
            }
            if(temp_in_progress){
            	groups.push(temp_in_progress)
            }
            if(temp_done){
            	groups.push(temp_done)
            }
            if(temp_cancel){
            	groups.push(temp_cancel)
            }
            if(temp_drop){
            	groups.push(temp_drop)
            }
            return groups
		},

		do_search: function(domain, context, group_by) {
			var self = this;
	        this.search_domain = domain;
	        this.search_context = context;
	        this.search_group_by = group_by;
	        return $.when(this.has_been_loaded).then(function() {
	            self.group_by = group_by.length ? group_by[0] : self.fields_view.arch.attrs.default_group_by;
	            self.group_by_field = self.fields_view.fields[self.group_by] || {};
	            self.grouped_by_m2o = (self.group_by_field.type === 'many2one');
	            self.$buttons.find('.oe_alternative').toggle(self.grouped_by_m2o);
	            self.$el.toggleClass('oe_kanban_grouped_by_m2o', self.grouped_by_m2o);
	            var grouping_fields = self.group_by ? [self.group_by].concat(_.keys(self.aggregates)) : undefined;
	            if (!_.isEmpty(grouping_fields)) {
	                // ensure group_by fields are read.
	                self.fields_keys = _.unique(self.fields_keys.concat(grouping_fields));
	            }
	            var grouping = new instance.web.Model(self.dataset.model, context, domain).query(self.fields_keys).group_by(grouping_fields);
	            return self.alive($.when(grouping)).then(function(groups) {
	                self.remove_no_result();
	                if (groups) {
	                	if (self.dataset.model == 'business.requirement'){
	                		groups = self.set_domain(groups)
	                	}
	                    return self.do_process_groups(groups);
	                } else {
	                    return self.do_process_dataset();
	                }
	            });
	        });
	    },
	})
}