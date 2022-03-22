odoo.define("business_requirement.tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    tour.register(
        "business_requirement_portal_tour",
        {
            test: true,
            url: "/my",
        },
        [
            {
                content: "Go /my/business_requirements url",
                trigger: 'a[href*="/my/business_requirements"]',
            },
            {
                content: "Go to BR item",
                trigger: ".tr_br_link:eq(0)",
            },
        ]
    );
});
