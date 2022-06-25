var hover = function () {
  $(".post-module").hover(function () {
    $(this).find(".description").stop().animate({
      height : "toggle",
      opacity: "toggle"
    }, 300);
  });
};
var rescreen = function () {
  var screenObj = screen.width;
  if (screenObj < 416) {
    $("#menu-toggle-2").click(function (e) {
      $("#sidebar-wrapper").toggleClass("toggled-2");
      $(".modulo").removeClass("ocultar").toggleClass("block");
    });
  }
};
$(document).ready(function () {
  var moduloActivado = $("#menu-content li:nth-child(2)");
  hover();
  rescreen();
  $("#moduloSelected").collapse("hide");
  var activos = $(".menu-content li");
  $(activos).click(function () {
    activos.removeClass("active");
    $(this).addClass("active");
  });
  $("#aparecer").toggleClass("hidden");
  $("#sidebar-wrapper").mouseover(function (e) {
    e.preventDefault();
    $("#over").addClass("opacidad sidenav-overlay");
    $("#wrapper").addClass("toggled-2");
    $(".hospital-sidebar").addClass("ocultar");
    $(".logo-box").addClass("logo-box2");
    $(".minsa").removeClass("ocultar");
    $(".logo-box p").addClass("logop2");
    $("#moduloSelected").collapse("show");
    $("#minsa-peque").attr("src", url_minsa_logo_grande).attr("id", "minsa-grande").addClass("minsa-grande");
  }).mouseleave(function () {
    $(".hospital-nombre").addClass("flexible").removeClass("ocultar");
    $("#wrapper").removeClass("toggled-2");
    $(".hospital-sidebar").removeClass("aparece");
    $("#over").removeClass("sidenav-overlay");
    $(".logo-box").removeClass("logo-box2");
    $(".minsa").addClass("ocultar");
    $(".logo-box p").removeClass("logop2");
    $("#moduloSelected").collapse("hide");
    $("#minsa-grande").attr("src", url_minsa_logo_peque).attr("id", "minsa-peque");
  });
  $("#menu-toggle-3").click(function (e) {
    $("#wrapper").toggleClass("toggled-3");
  });
});
