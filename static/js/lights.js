var prev = null;

function change_handler(value) {
	hide_settings();
	if (value !== prev) {
		prev = value;
	}

	if (value == "rainbow-circle") {
		show_setting("speed");
		show_setting("offset");
	} else if (value == "animated-rainbow") {
		show_setting("speed");
	} else if (value == "pixel-pileup") {
		show_setting("color-picker");
		show_setting("speed");
	} else if (value == "rainbow-pixel-pileup") {
		show_setting("speed");
		show_setting("offset");
	} else if (value == "pixel-run") {
		show_setting("color-picker");
		show_setting("speed");
	} else if (value == "rainbow-pixel-run") {
		show_setting("speed");
		show_setting("offset");
	} else if (value == "solid-color") {
		show_setting("color-picker");
	} 
}

function show_setting(name) {
	document.getElementById(name).style.display = "inline-block";
	document.getElementById(name.concat("-label")).style.display = "block";
}

function hide_settings() {
	document.getElementById("speed").style.display = "none";
	document.getElementById("speed-label").style.display = "none";

	document.getElementById("color-picker").style.display = "none";
	document.getElementById("color-picker-label").style.display = "none";

	document.getElementById("offset").style.display = "none";
	document.getElementById("offset-label").style.display = "none";
}