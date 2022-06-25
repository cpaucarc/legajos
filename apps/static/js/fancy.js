/**
 * Created by cj on 2/2/17.
 */
$(document).ready(function () {
  $("div.panel-active").mouseenter(function () {
    $(this).removeClass("panel-default").addClass("panel-primary");
  }).mouseleave(function () {
    $(this).addClass("panel-default").removeClass("panel-primary");
  });

  $(".panel-collapse").on("click", function () {
    if ($(this).data("collapsed")) {
      $("#collapsible-" + $(this).prop("id")).slideDown();
      $(this).data("collapsed", false);
      $(this).find(".fa").removeClass("fa-expand").addClass("fa-compress");
    } else {
      $("#collapsible-" + $(this).prop("id")).slideUp();
      $(this).data("collapsed", true);
      $(this).find(".fa").removeClass("fa-compress").addClass("fa-expand");
    }
  }).each(function (i, e) {
    if ($(e).data("collapsed")) {
      $(e).find(".panel-title").prepend("<i class='fa fa-expand'></i> &nbsp;");
      $("#collapsible-" + $(e).prop("id")).slideUp();
    } else {
      $(e).find(".panel-title").prepend("<i class='fa fa-compress'></i> &nbsp;");
      $("#collapsible-" + $(e).prop("id")).slideDown();
    }
  });
});
