var nombre;
var email;
var password;
var formato_email = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
function validarFormulario(){
    nombre = document.getElementById("nombre").value;
    email = document.getElementById("correo").value;
    password = document.getElementById("password").value;
    console.log(email);

    if(nombre.length == 0 || nombre.length < 8){
        alert("Debes ingresar un nombre de usuario de mínimo 8 caracteres!!!");
        nombre.focus();
        return false;
    }

    if(!email.match(formato_email)){
        alert("Debes ingresar un correo electrónico válido (xyz@midominio.com)!!!");
        email.focus();
        return false;
    }

    if(password.length == 0 || password.length < 8){
        alert("Debes ingresar una contraseña de más de 8 caracteres!!!");
        password.focus();
    }
}
function mostrarPassword(){
    document.getElementById("password").setAttribute('type','text');
}
function ocultarPassword(){
    document.getElementById("password").setAttribute('type','password');
}