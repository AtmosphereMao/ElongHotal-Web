function c(i) {
	try {
		var d = $("#tsd").val();
		if (null == d || "" === d || !d) return - 99;
		var a = this.d(d, i),
		script = eval(this.h(a));
		return script
	} catch(e) {
		return this.g()
	}
}

function h(script) {
	return null == script || "" === script ? script: script.replace(/\)\^-1/gm, ")&-1")
}

function d(s, i) {
	var decipher = crypto.createDecipheriv(this.v(), this.k(i), window.Globals.cookie("iv")),
	decrypted = decipher.update(s, "hex", "binary");
	return decrypted += decipher["final"]("binary"),
	null != decrypted && "" !== decrypted && decrypted ? decrypted: ""
}

function g() {
	return Math.ceil(1e7 * Math.random())
}

function k(i) {
	for (var m = "",
	v = 0; v < 16 - (i + "a").length; v += 1) m += "a";
	return i + "a" + m
}

function v() {
	var a = "es",
	b = "bc";
	return "a" + a + "-128-c" + b
}
c(179900)