const errorForm = document.querySelector(".form-error");
const usernameInput = document.getElementById("id_username");
const emailInput = document.getElementById("id_email");
const passwordInput = document.getElementById("id_password");
const codAreaSelect = document.getElementById("id_cod_area");
const nacimientoInput = document.getElementById("id_fecha_nacimiento");
const nombreInput = document.getElementById("id_first_name");
const apellidoInput = document.getElementById("id_last_name");
const telefonoInput = document.getElementById("id_telefono");
const btnStep1 = document.getElementById("btn-siguiente-step1");
const btnStep2 = document.getElementById("btn-siguiente-step2");
const formSignup = document.getElementById("form-signup")


function activarCarga() {
  document.querySelector(".btn-text").classList.add('hidden');  
  document.querySelector(".spinner").classList.remove('hidden');   
}

function cambiarCodigo() {
  let codigo_actual = document.getElementById("id_cod_area").value
  document.getElementById("codigo_area").innerText = codigo_actual;
}

document.addEventListener("DOMContentLoaded", function () {
  const inputs = document.querySelectorAll(".input-form-box input");  // Selecciono los inputs dentro de .input-form-box

  inputs.forEach(input => {
    // Evita escribir espacios al presionar la barra espaciadora :
    input.addEventListener("keydown", function (e) {   
      if (e.key === " ") {
        e.preventDefault();
      }
    });
  });

  // Validación para el campo de 'Nombre de usuario' (solo letras y números)
  if (usernameInput) {
    usernameInput.addEventListener("input", function () {

      let inputValue = this.value;
      this.value = inputValue.replace(/[^a-zA-ZñÑ0-9._-]/g, "").slice(0, 20); // Solo letras, números, . , - , -

      const usernameFeedback = document.getElementById("usernameFeedback");
      if(usernameFeedback){
        usernameInput.classList.remove("error");
        usernameFeedback.textContent = "";
      }
    });
  }

  // Validación para el campo de 'Correo electrónico' (solo caracteres válidos para emails)
  if (emailInput) {
    emailInput.addEventListener("input", function () {
      let inputValue = this.value;
      this.value = inputValue.replace(/[^a-zA-ZñÑ0-9@._\-!#$%&'*+/=?^`{|}~]/g, ""); // Solo caracteres válidos para email (letras,numeros,@ . _ - ! # $ % & ' * + / = ? ^ \ { | } ~`)

      const emailFeedback = document.getElementById("emailFeedback");
      if(emailFeedback){
        emailInput.classList.remove("error");
        emailFeedback.textContent = "";
      }
    });
  }

  // Validación para el campo de 'Contraseña' (mínimo 6 caracteres, al menos una letra mayúscula y un número)
  if (passwordInput) {
    passwordInput.addEventListener("input", function () {

      const passwordPattern = /^(?=.*[A-Za-zñÑ])(?=.*[A-ZñÑ])(?=.*\d)[A-Za-zñÑ\d._@#$%&*!?-]{6,}$/; // La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -
      const passwordFeedback = document.getElementById("passwordFeedback");

      if (!passwordPattern.test(this.value)) {
        if (passwordFeedback) {
          passwordFeedback.textContent = "La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -";
          passwordFeedback.style.color = "red";
        }
      } 
      else {
        if (passwordFeedback) {
          passwordInput.classList.remove("error");
          passwordFeedback.textContent = "";
        }
      }
    });
  }

  if (codAreaSelect) {
    codAreaSelect.addEventListener("change", function () {
      let selectedValue = this.value;
      if(selectedValue != ""){
        codAreaSelect.classList.remove("error");
      }

    });
  }


  if (nacimientoInput) {
    const fecha_actual = new Date();
    const minimoEdad = 18;

    fecha_actual.setFullYear(fecha_actual.getFullYear() - minimoEdad);
    const fecha_maxima = fecha_actual.toISOString().split('T')[0];
    nacimientoInput.setAttribute("max", fecha_maxima);

  }


  // Validación para el campo de 'Nombre' (solo letras)
  if (nombreInput ) {
    nombreInput.addEventListener("input", function () {
      let inputValue = this.value;
      
      inputValue = inputValue.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ]/g, ""); // Solo letras, tildes, ñ
        
      if (inputValue.length > 0) {
        inputValue = inputValue.charAt(0).toUpperCase() + inputValue.slice(1).toLowerCase();  // Convierte primera letra en mayúscula y el resto en minúsculas
      }
      this.value = inputValue;
    });
  }

  // Validación para el campo de 'apellido' (solo letras)
  if (apellidoInput) {
    apellidoInput.addEventListener("input", function () {
    let inputValue = this.value;

    inputValue = inputValue.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ]/g, ""); // Solo letras, tildes, ñ
  
    if (inputValue.length > 0) {
      inputValue = inputValue.charAt(0).toUpperCase() + inputValue.slice(1).toLowerCase();  // Convierte primera letra en mayúscula y el resto en minúsculas;
    }
    this.value = inputValue; 
    });
  }

  // Validación para el campo de 'telefono' (solo numeros)

  if (telefonoInput) {
    telefonoInput.addEventListener("input", function () {
      this.value = this.value.replace(/[^0-9]/g, "").slice(0, 8);  // Elimina del input todo lo que no sean numeros y con el slice limitamos la cantidad maxima de caracteres a 8.
  
      const telefonoPattern = /^[0-9]{6,8}$/;  // Expresion regula que luego utilizamos para validar que solo sean numeros, de entre 6 y 8 digitos
      const telefonoFeedback = document.getElementById("telefonoFeedback");
  
      if (!telefonoPattern.test(this.value)) {
        if (telefonoFeedback) {
          telefonoFeedback.textContent = "El número de teléfono debe contener entre 6 y 8 dígitos.";
          telefonoFeedback.style.color = "red";
        }
      } else {
        if (telefonoFeedback) {
          telefonoFeedback.textContent = "";
        }
      }
    });
  }
  if(formSignup){
    cambiarCodigo(); 
  }

});


const inputs_step1 = document.querySelectorAll("#step1 input,select"); 
const inputs_step2 = document.querySelectorAll("#step2 input,select"); 
const allInputs = document.querySelectorAll('input[required], select[required]');

inputs_step1.forEach(input => {
  input.addEventListener('input', checkIfAllValid);
});

inputs_step2.forEach(input => {
  input.addEventListener('input', checkIfAllValid);
});

allInputs.forEach(input => {
  input.addEventListener('input', checkIfAllValid);
  input.addEventListener('change', checkIfAllValid); // importante para el checkbox
});

function checkIfAllValid() {
  let isCompletados = true;
  let isCompletadosStep1 = true;
  let isCompletadosStep2 = true;

  inputs_step1.forEach(field => {
    if (!field.value) {
      isCompletadosStep1 = false;
    }
  });

  inputs_step2.forEach(field => {
    if (!field.value) {
      isCompletadosStep2 = false;
    }
  });

  allInputs.forEach(field => {
    if (field.type === 'checkbox') {
      if (!field.checked) {
        isCompletados = false;
      }
    } else if (!field.value) {
      isCompletados = false;
    }
  });


  if(formSignup){
  document.getElementById("btn-registro").disabled = !isCompletados;
  btnStep1.disabled = !isCompletadosStep1;
  btnStep2.disabled = !isCompletadosStep2;
  }
}

// Función para validar los campos de cada paso 
function validateStep(stepNumber) {
    let valid = true;
    let valid_username = true;
    let valid_email = true;
    let valid_contraseña = true;
    let valid_nombre = true;
    let valid_edad = true;
    let valid_apellido = true;
    let valid_telefono = true;
    const step = document.getElementById(`step${stepNumber}`);
    const inputs = step.querySelectorAll('input[required], select[required]');  // Seleccionamos todos los campos requeridos

    
    // Verificar cada campo
    inputs.forEach(input => {

      if (!input.value) { // Si el input esta vacio :
        valid = false;
        input.classList.add('error');  // Agregar una clase de error si el campo está vacío
      } else {
        input.classList.remove('error');  // Eliminar la clase de error si el campo está completo
      }

    });
  
    if(stepNumber == 1){
      if (usernameInput) {
        const usernameRegex = /^(?=.*[A-Za-z]).*$/; // La nombre de usuario debe tener por lo menos una letra
        if(!usernameRegex.test(usernameInput.value)){
          valid_username = false
        }
      }
  
      if (emailInput){
        const emailRegex = /^(?!\.)[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,}$/;
        if(!emailRegex.test(emailInput.value)){
          valid_email = false;
        }
        // (?!\.)  Asegura que el correo NO comience con un punto (lookahead negativo).
        // [\w!#$%&'*+/=?^_`{|}~-]+   Uno o más caracteres válidos para el nombre de usuario (local-part). Incluye letras, números y caracteres especiales permitidos.
        // (?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*  Permite puntos dentro del nombre de usuario, pero no consecutivos ni al inicio o final.  Agrupado como parte no capturada y puede repetirse cero o más veces.
        // @  El carácter arroba, separador obligatorio entre usuario y dominio.
        // (?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+    Valida uno o más subdominios:  - Cada parte del dominio debe comenzar y terminar con una letra o número. - Puede contener guiones, pero no al inicio/final de cada fragmento. - Limita a 63 caracteres por subdominio (por la parte `{0,61}` con caracteres al inicio y fin).
        //  [A-Za-z]{2,}   La extensión del dominio debe tener al menos dos letras (como `.com`, `.org`, `.io`, etc.).
        // $  Final de la cadena. Asegura que toda la cadena sea un email completo y no contenga basura extra.


      } 
  
      if (passwordInput){
        const passwordRegex = /^(?=.*[A-Za-zñÑ])(?=.*[A-ZñÑ])(?=.*\d)[A-Za-zñÑ\d._@#$%&*!?-]{6,}$/;  // La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -
        if(!passwordRegex.test(passwordInput.value)){
          valid_contraseña = false;
        }
      } 
      return [valid,valid_username,valid_email,valid_contraseña];
    }

    if(stepNumber == 2){
      
      if (nacimientoInput) {
        const fecha_actual = new Date();
        const minimoEdad = 18;
    
        fecha_actual.setFullYear(fecha_actual.getFullYear() - minimoEdad);
        const fecha_maxima = fecha_actual.toISOString().split('T')[0];
        nacimientoInput.setAttribute("max", fecha_maxima);
    
        if (nacimientoInput.value) {
          const fecha_seleccionada = new Date(nacimientoInput.value);
          const fecha_minima = new Date(fecha_maxima);
    
          if (fecha_seleccionada > fecha_minima) {
            valid_edad = false;
          }
        }
      }

      if (nombreInput) {
        const nombreRegex = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{1,}$/; 
        if(!nombreRegex.test(nombreInput.value)){
          valid_nombre = false
        }
      }

      if (apellidoInput) {
        const apellidoRegex = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{1,}$/; 
        if(!apellidoRegex.test(apellidoInput.value)){
          valid_apellido = false
        }
      }

      if (telefonoInput){
        const telefonoRegex =  /^[0-9]{6,8}$/; 
        if(!telefonoRegex.test(telefonoInput.value)){
          valid_telefono = false;
        }
      }       

      return [valid,valid_edad,valid_nombre,valid_apellido,valid_telefono];
    }    

  }


function nextStep(stepNumber) {    // Función para pasar al siguiente paso
    const usernameFeedback = document.getElementById("usernameFeedback");
    const emailFeedback = document.getElementById("emailFeedback");
    const passwordFeedback = document.getElementById("passwordFeedback");
    const nacimientoFeedback = document.getElementById("nacimientoFeedback");
    const nombreFeedback = document.getElementById("nombreFeedback");
    const apellidoFeedback = document.getElementById("apellidoFeedback");

    if(stepNumber == 1){
      const [isValid,isValid_username, isValid_email, isValid_contraseña] = validateStep(stepNumber)
      usernameFeedback.textContent = "";
      emailFeedback.textContent = "";

      if (isValid && isValid_username && isValid_email && isValid_contraseña) {   // Si el paso es válido, avanzamos al siguiente paso

        const currentStep = document.getElementById(`step${stepNumber}`);
        currentStep.classList.remove('active');
  
        const nextStep = document.getElementById(`step${stepNumber + 1}`);
        nextStep.classList.add('active');
      }
      else{
        if (!isValid_username ){
          usernameFeedback.textContent = "Tu nombre de usuario debe contener por lo menos una letra."
          usernameFeedback.style.color = "red";  
        }
        if (!isValid_email) {
          emailFeedback.textContent = "El email ingresado no es valido."
          emailFeedback.style.color = "red";  
        }
        if(!isValid_contraseña ){
          passwordFeedback.textContent = "La contraseña debe tener al menos 6 caracteres, una letra mayúscula y un número."
          passwordFeedback.style.color = "red";  
        }

      }
    }

    if(stepNumber == 2){
      const [isValid,isValid_edad,isValid_nombre,isValid_apellido,isValid_telefono] = validateStep(stepNumber);
      nombreFeedback.textContent = "";
      apellidoFeedback.textContent = "";
      nacimientoFeedback.textContent = "";

      if (isValid && isValid_edad && isValid_nombre && isValid_apellido && isValid_telefono) {   // Si el paso es válido, avanzamos al siguiente paso

        const currentStep = document.getElementById(`step${stepNumber}`);
        currentStep.classList.remove('active');
  
        const nextStep = document.getElementById(`step${stepNumber + 1}`);
        nextStep.classList.add('active');
      }
      else{
        if (!isValid_edad){
          nacimientoFeedback.textContent = "La fecha seleccionada es demasiado reciente. Debes ser mayor de 18 años.";
          nacimientoFeedback.style.color = "red";  
        }
        if (!isValid_nombre){
          nombreFeedback.textContent = "Debe haber por lo menos 2 caracteres."
          nombreFeedback.style.color = "red";  
        }
        if (!isValid_apellido ){
          apellidoFeedback.textContent = "Debe haber por lo menos 2 caracteres."
          apellidoFeedback.style.color = "red";  
        }
        if (!isValid_telefono){
          telefonoFeedback.textContent = "El número de teléfono debe contener entre 6 y 8 dígitos.";
          telefonoFeedback.style.color = "red";  
        }                        

      }
    }
  

  }

  
  // Función para retroceder al paso anterior
function prevStep(stepNumber) {
    const currentStep = document.getElementById(`step${stepNumber}`);
    currentStep.classList.remove('active');
  
    const prevStep = document.getElementById(`step${stepNumber - 1}`);
    prevStep.classList.add('active');
}

// Mostrar el primer paso por defecto
if(formSignup){
  document.getElementById('step1').classList.add('active');
}



// Ocultar errores de Django al modificar campos
document.querySelectorAll("#form-signup input, #form-signup select").forEach(input => {
  input.addEventListener("input", () => {
    const errorLists = input.parentElement.querySelectorAll(".form-errors");


    errorLists.forEach(error => error.remove());

    const cant_errores = document.querySelectorAll(".form-errors");  
    if (cant_errores.length === 0 && errorForm) { 
      errorForm.remove(); 
    }
  });
});
