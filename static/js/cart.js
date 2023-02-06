function addTip(tip) {
  document.getElementsByName('tip')[0].value = tip
}
function addRequired() {
  document.getElementById("tip").required = true;
  document.getElementById("confirmation").required = true;
}
function deleteRequired() {
  document.getElementById("tip").required = false;
  document.getElementById("confirmation").required = false;
}
function displayTotalAfterTip(tip, prevTotal) {
  addTip(tip)
  if (!tip) {
    tip = 0
  }
  document.getElementById('total-after-tip').style.display = ''
  document.getElementById('total-after-tip-value').innerHTML = '$' + (parseFloat(tip)+parseFloat(prevTotal)).toFixed(2);
}