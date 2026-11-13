import {registry} from "@web/core/registry";

registry
    .category("web_tour.tours")
    .add("business_requirement_deliverable_portal_tour", {
        url: "/my",
        steps: () => [
            {
                content: "Go /my/brd url",
                trigger: 'a[href*="/my/brd"]',
                run: "click",
                expectUnloadPage: true,
            },
            {
                content: "Go to BRD item",
                trigger: ".tr_brd_link:first",
                run: "click",
                expectUnloadPage: true,
            },
        ],
    });
