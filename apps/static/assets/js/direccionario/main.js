document.addEventListener('DOMContentLoaded', iniciar);

function validarTextoEntrada(input, patron) {
    var texto = input.value;
    var letras = texto.split("");

    for (var x in letras) {
        var letra = letras[x];

        if (!(new RegExp(patron, "i")).test(letra)) {
            letras[x] = "";
        }
    }

    input.value = letras.join("");
}

// Corregido: Iterar sobre la colección para añadir el evento a cada elemento.
var txtSoloNumeros = document.getElementsByClassName("soloNum");
for (const element of txtSoloNumeros) {
    element.addEventListener("input", function (event) {
        validarTextoEntrada(this, "[0-9]");
    });
}

// Corregido: Aplicar la misma lógica a los otros elementos.
var txtSoloLetras = document.getElementsByClassName("soloText");
for (const element of txtSoloLetras) {
    element.addEventListener("input", function (event) {
        validarTextoEntrada(this, "[a-z ]");
    });
}

var txtPersonalizado = document.getElementsByClassName("textNum");
for (const element of txtPersonalizado) {
    element.addEventListener("input", function (event) {
        validarTextoEntrada(this, "[0-9a-z]");
    });
}

var txtPersonalizado2 = document.getElementsByClassName("email");
for (const element of txtPersonalizado2) {
    element.addEventListener("input", function (event) {
        validarTextoEntrada(this, "[/^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/ ]");
    });
}

function iniciar() {
    var txtCurp = document.querySelectorAll('.mayusc');
    txtCurp.forEach(ele => ele.addEventListener('input', function (event) {
        this.value = this.value.toUpperCase();
    }));
}

// Corregido: Esta sección estaba duplicada y mal implementada.
// Se ha eliminado la llamada redundante y se ha movido la lógica al bucle en la función `iniciar` para evitar duplicaciones.

var txtUsuario = document.getElementsByClassName("txtUsuario");
for (const element of txtUsuario) {
    element.addEventListener("input", function (event) {
        this.value = this.value.toLowerCase();
    });
}

// Se han eliminado las funciones comentadas ya que no eran parte del problema original y no son utilizadas en el código principal.