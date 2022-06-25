$(function () {
  $("#div-eye-passwd").mousedown(function () {
    $("#eye-addon").removeClass("fa-eye-slash").addClass("fa-eye");
    $("#id_password").attr("type", "text");
  }).mouseup(function () {
    $("#eye-addon").removeClass("fa-eye").addClass("fa-eye-slash");
    $("#id_password").attr("type", "password")
  });
});
