$(function () {
    $("#header").load("header");
});

$(function () {
    $("#coop-query").load("/coop_query?" + $.param({ category: "all" }));
})

function showCategory(variable) {
    $("#coop-query").load("/coop_query?" + $.param({ category: variable }));
}