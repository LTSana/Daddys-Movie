
document.querySelectorAll(".alert").forEach(button => {
	button.querySelectorAll(".close").forEach(close_box => {
		close_box.onclick = () => {
			button.classList.toggle("d-flex", false);
			button.classList.toggle("d-none", true);
		}
	})
});

ALERT_MESSAGE = (alert_id, message) => {
	/* 
	Alert ID of the alert box you want to trigger.
	Message the information of the alert
	 */
	document.querySelector(`${alert_id} > .alert-text`).innerHTML = message;
	document.querySelector(`${alert_id}`).classList.toggle(`d-none`, false);
	document.querySelector(`${alert_id}`).classList.toggle(`d-flex`, true);
}