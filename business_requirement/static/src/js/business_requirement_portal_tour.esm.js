import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("business_requirement_portal_tour", {
    url: "/my",
    steps: () => [
        {
            content: "Go /my/business_requirements url",
            trigger: 'a[href*="/my/business_requirements"]',
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Go to BR item",
            trigger: ".tr_br_link:first",
            run: "click",
            expectUnloadPage: true,
        },
    ],
});
