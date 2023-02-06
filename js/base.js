// When the user clicks on <span> (x), close the modal
function closeMsgModal() {
    document.getElementById("msg-modal-id").style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
    var modal = document.getElementById("msg-modal-id");
    if (event.target == modal) {
        modal.style.display = "none";
    }
})