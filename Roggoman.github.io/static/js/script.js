function hel() {
    var word = "0000"
    var pass = document.querySelector("#pass").value;
    if (word != pass) {
        alert(['"' + pass + '" - неверный пароль'])
    }
}