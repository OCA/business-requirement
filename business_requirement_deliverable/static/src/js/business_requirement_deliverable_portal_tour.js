odoo.define("business_requirement_deliverable.tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    tour.register(
        "business_requirement_deliverable_portal_tour",
        {
            test: true,
            url: "/my",
        },
        [
            {
                content: "Go /my/brd url",
                trigger: 'a[href*="/my/brd"]',
            },
            {
                content: "Go to BRD item",
                trigger: ".tr_brd_link:eq(0)",
            },
        ]
    );
});
