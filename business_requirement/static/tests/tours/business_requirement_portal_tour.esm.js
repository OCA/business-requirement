/** @odoo-module */

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("business_requirement_portal_tour", {
    test: true,
    url: "/my",
    steps: () => [
        {
            content: "Go /my/business_requirements url",
            trigger: 'a[href*="/my/business_requirements"]',
        },
        {
            content: "Go to BR item",
            trigger: ".tr_br_link:eq(0)",
        },
    ],
});
