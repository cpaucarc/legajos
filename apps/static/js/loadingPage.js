/**
 * Created by cj on 2/14/17.
 */
function onReady(callback) {
  var intervalID = window.setInterval(checkReady, 500);

  function checkReady() {
    if (document.getElementsByTagName("body")[0] !== undefined) {
      window.clearInterval(intervalID);
      callback.call(this);
    }
  }
}

function show(id, value) {
  document.getElementById(id).style.display = value ? "block" : "none";
}

onReady(function () {
  show("page", true);
  show("loading", false);
  NProgress.done();
});
