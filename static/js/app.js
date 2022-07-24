$(function () {
    $("#header").load("header");
});

$(function () {
    $("#coop-query").load("/coop_query?" + $.param({ category: "all" }));
})

function showAll() {
    $("#coop-query").load("/coop_query?" + $.param({ category: "all" }));
}

function showAFS() {
    $("#coop-query").load("/coop_query?" + $.param({ category: "Accomodations and Food Service" }));
}

function showHC() {
    $("#coop-query").load("/coop_query?" + $.param({ category: "Health Care" }));
}
function showME() {
    $("#coop-query").load("/coop_query?" + $.param({ category: "Manufacturing and Engineering" }));
}
function showTech() {
    $("#coop-query").load("/coop_query?" + $.param({ category: "Technology" }));
}
function showDesign() {
    $("#coop-query").load("/coop_query?" + $.param({ category: "Design" }));
}

