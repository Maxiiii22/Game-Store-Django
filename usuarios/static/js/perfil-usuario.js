const modal = document.getElementById("editModal");
const closeModalBtn = document.getElementById("closeEditModal");
const modalInput = document.getElementById("modalInput");
const modalSelect = document.getElementById("modalSelect");
const modalDate = document.getElementById("modalDate");
const modalTel = document.getElementById("modalTel");
const modalTitle = document.getElementById("modal-title");
const modalField = document.getElementById("modalField");
const btnGuardar = document.querySelector(".btn-guardar");
const errorModal = document.querySelector(".form-error-modal");
const telefonoInput = document.getElementById('modalTel');
const inputFeedback = document.getElementById('inputFeedback');


function UsernameInput(e) {
    let inputValue = e.target.value;
    e.target.value = inputValue.replace(/[^a-zA-ZñÑ0-9._-]/g, "").slice(0, 20); // Solo letras, números, . , - , -
}

function EmailInput(e) {
    let inputValue = e.target.value;
    e.target.value = inputValue.replace(/[^a-zA-ZñÑ0-9@._\-!#$%&'*+/=?^`{|}~]/g, ""); // Solo caracteres válidos para email (letras,numeros,@ . _ - ! # $ % & ' * + / = ? ^ \ { | } ~`)
}

function PasswordInput(e) {
    const passwordPattern = /^(?=.*[A-Za-zñÑ])(?=.*[A-ZñÑ])(?=.*\d)[A-Za-zñÑ\d._@#$%&*!?-]{6,}$/; // La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -
    const inputFeedback = document.querySelector("#inputFeedback");

    if (!passwordPattern.test(e.target.value)) {
        if (inputFeedback) {
            inputFeedback.textContent = "La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -";
        }
    } else {
        if (inputFeedback) {
            inputFeedback.textContent = "";
        }
    }
}

function NameInput(e) {
    let inputValue = e.target.value;
    inputValue = inputValue.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ]/g, ""); // Solo letras, tildes, ñ
    if (inputValue.length > 0) {
        e.target.value= inputValue.charAt(0).toUpperCase() + inputValue.slice(1);
    } 
    else {
        e.target.value = inputValue; 
    }
}

function generarInputCampoModal(campo, valor = "", valorPassword = "", opciones = []) {
    const editForm = document.getElementById("editForm");
    const modalTitle = document.getElementById("modal-title");
    const inputFeedback = document.getElementById("inputFeedback");

    // Eliminar inputs existentes
    let inputModal = document.getElementById("input_modal");
    if (inputModal) inputModal.remove();

    let inputNewPassword = document.getElementById("newPassword");
    if (inputNewPassword) inputNewPassword.remove();

    // Creador de inputs
    const crearInput = (type, placeholder, name, value = "", required = true) => {
        const input = document.createElement("input");
        input.type = type;
        input.placeholder = placeholder;
        input.name = name;
        input.id = name === "new_valor" ? "input_modal" : "newPassword";
        input.className = "modal-input";
        input.value = value;
        if (required) input.required = true;
        return input;
    };

    // Campo: username
    if (campo === "username") {
        modalTitle.textContent = "Editar Nombre de usuario:";
        inputModal = crearInput("text", "Ingrese un nombre de usuario", "new_valor", valor);
        inputModal.addEventListener("input", UsernameInput);
        editForm.insertBefore(inputModal, editForm.children[3]);
    }

    // Campo: email
    else if (campo === "email") {
        modalTitle.textContent = "Editar Correo electrónico:";
        inputModal = crearInput("email", "Ingrese un email", "new_valor", valor);
        inputModal.addEventListener("input", EmailInput);
        editForm.insertBefore(inputModal, editForm.children[3]);
    }

    // Campo: password
    else if (campo === "password") {
        modalTitle.textContent = "Editar Contraseña:";
        inputModal = crearInput("password", "Ingrese su contraseña actual", "new_valor", "");
        inputNewPassword = crearInput("password", "Ingrese la nueva contraseña", "new_password", valorPassword);
        inputNewPassword.addEventListener("input", PasswordInput);
        editForm.insertBefore(inputModal, editForm.children[3]);
        editForm.insertBefore(inputNewPassword, editForm.children[4]);
    }

    // Campo: nombre o apellido
    else if (campo === "first_name" || campo === "last_name") {
        modalTitle.textContent = campo === "first_name" ? "Editar Nombre:" : "Editar Apellido:";
        const placeholder = campo === "first_name" ? "Ingrese su nombre" : "Ingrese su apellido";
        inputModal = crearInput("text", placeholder, "new_valor", valor);
        inputModal.addEventListener("input", NameInput);
        editForm.insertBefore(inputModal, editForm.children[3]);
    }

    // Campo: fecha de nacimiento
    else if (campo === "fecha_nacimiento") {
        modalTitle.textContent = "Editar Fecha de nacimiento:";
        inputModal = crearInput("date", "", "new_valor", valor);
        const fecha_actual = new Date();
        fecha_actual.setFullYear(fecha_actual.getFullYear() - 18);
        inputModal.max = fecha_actual.toISOString().split("T")[0];
        editForm.insertBefore(inputModal, editForm.children[3]);
    }

    // Campo: código de área
    else if (campo === "cod_area") {
        modalTitle.textContent = "Editar Código de área:";
        const select = document.createElement("select");
        select.id = "input_modal";
        select.name = "new_valor";
        select.className = "modal-input";
        select.required = true;

        const options = Array.from(modalSelect.options);   // Guardamos las opciones del sourceSelect en una variable

        options.forEach(optionElement => {
            const option = document.createElement("option");
            option.value = optionElement.value;
            option.textContent = optionElement.text;
            if (valor === optionElement.value) option.selected = true;
            select.appendChild(option);
        });

        editForm.insertBefore(select, editForm.children[3]);
    }

    // Campo: teléfono
    else if (campo === "telefono") {
        modalTitle.textContent = "Editar Teléfono:";
        inputModal = crearInput("text", "Ingrese un número de teléfono", "new_valor", valor);
        inputModal.inputMode = "numeric";
        inputModal.addEventListener("input", function () {
            this.value = this.value.replace(/[^0-9]/g, "").slice(0, 8);
            const telefonoPattern = /^[0-9]{6,8}$/;
            if (!telefonoPattern.test(this.value)) {
                inputFeedback.textContent = "El número de teléfono debe contener entre 6 y 8 dígitos.";
            } else {
                inputFeedback.textContent = "";
            }
        });
        editForm.insertBefore(inputModal, editForm.children[3]);
    }

    return { inputModal, inputNewPassword };
}


function mostrarModalConError({ campo_modal, error, campo_valor, campo_valor_password = "",error_new_password, opciones_cod_area = [] }) {
    const modal = document.getElementById("editModal");
    const modalField = document.getElementById("modalField");
        
    modal.classList.add("show");
    modalField.value = campo_modal;
    inputFeedback.textContent = error;
    let error_new_passwordd;
    error_new_passwordd = error_new_password;
        
    const { inputModal, inputNewPassword } = generarInputCampoModal(campo_modal,campo_valor,campo_valor_password,opciones_cod_area);

    if (error_new_passwordd == true) {
        inputNewPassword.classList.add("error");
    } 
    else{
        inputModal.classList.add("error");
    }
}


document.addEventListener("DOMContentLoaded", function () {
    if (window.modalData) {
        mostrarModalConError(window.modalData);
    }

    modalSelect.remove()


    document.querySelectorAll(".datos-campos_input").forEach(input => {
        modalSelect.remove()


        input.addEventListener("click", () => {
            const inputSeleccionado = input.id;
            const inputValor = input.value;
            modalField.value = inputSeleccionado;
            
            const { inputModal, inputNewPassword } = generarInputCampoModal( inputSeleccionado, inputValor);

            modal.classList.add("show");
            document.body.style.overflow = "hidden";

        });
    });


});


closeModalBtn.addEventListener("click", () => {
    modal.classList.remove("show");
    document.body.style.overflow = "auto";
    inputFeedback.textContent = "";
    const inputModal = document.getElementById("input_modal");
    const inputNewPassword = document.getElementById("newPassword");
    if (inputModal) {
        inputModal.remove();
    }
    if (inputNewPassword) {
        inputNewPassword.remove();
    }    
    
});

window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.classList.remove("show");
        document.body.style.overflow = "auto";
        inputFeedback.textContent = "";

        const inputModal = document.getElementById("input_modal");
        const inputNewPassword = document.getElementById("newPassword");
        if (inputModal) {
            inputModal.remove();
        }
        if (inputNewPassword) {
            inputNewPassword.remove();
        }

    }
});


/**
 * Valida un campo mediante una consulta AJAX GET.
 * @param {string} url - La URL a la que se hace la consulta, con parámetros GET.
 * @param {HTMLElement} feedbackElement - Elemento donde mostrar mensajes de error.
 * @param {string} mensajeErrorDefault - Mensaje a mostrar si no hay mensaje del backend.
 * @param {function} onSuccess - Callback a ejecutar si la validación es exitosa.
 * @param {function} [onError] - Callback opcional si la validación falla.
 */
function validarCampoAjax(url, feedbackElement, mensajeErrorDefault, onSuccess, onError) {
    const inputModal = document.getElementById("input_modal");
    fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.available || data.success || data.correct) {
            feedbackElement.textContent = "";
            if (onSuccess) onSuccess(data);
        } else {
            feedbackElement.style.color = "red";
            inputModal.classList.add('error');
            feedbackElement.textContent = data.error || mensajeErrorDefault;
            if (onError) onError(data);
        }
    })
    .catch(() => {
        feedbackElement.textContent = "⚠️ Error de conexión al validar.";
        feedbackElement.style.color = "orange";
        if (onError) onError();
    });
}

modal.addEventListener("submit", function(event) {
    event.preventDefault();

    const allinputsModal = document.querySelectorAll(".modal-input");
    const inputModal = document.getElementById("input_modal");
    const inputnewPassword = document.getElementById("newPassword");
    const campoSeleccionado = modalField.value;

    allinputsModal.forEach(input => {
        if (!input.value.trim()) {
            console.log("todosInputs")
            inputFeedback.textContent = "Por favor, complete todos los campos.";
            input.classList.add('error');
        }
    }); 

    inputModal.addEventListener("input", () => {
        inputFeedback.textContent = "";
        inputModal.classList.remove('error');
    });
    
    if(inputnewPassword){
        inputnewPassword.addEventListener("input", () => {
            inputFeedback.textContent = "";
            inputnewPassword.classList.remove('error');
        });
    }
    
    if (!inputModal.value.trim()) {
        console.log("Inputs")
        inputFeedback.textContent = "Por favor, complete todos los campos.";
        inputModal.classList.add('error');
        return;
    }


    if(campoSeleccionado === "username"){
        const usernameRegex = /^(?=.*[A-Za-z]).*$/; // La nombre de usuario debe tener por lo menos una letra
        if(!usernameRegex.test(inputModal.value)){
            inputFeedback.textContent = "Tu nombre de usuario debe contener por lo menos una letra.";
            inputModal.classList.add('error');
            return;
        }
        const url = `/usuario/mi-cuenta/?username=${encodeURIComponent(inputModal.value)}`;  // encodeURIComponent() al insertar datos de entrada en la URL, evita errores con caracteres especiales (@, &, =, etc.).
        validarCampoAjax(url, inputFeedback, "El nombre de usuario ya está en uso.", () => {
            document.getElementById("editForm").submit();
        });                
    }   
    else if (campoSeleccionado === "email") {
        const emailRegex = /^(?!\.)[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,}$/;
        if(!emailRegex.test(inputModal.value)){
            inputFeedback.textContent = "El email ingresado no es valido.";
            inputModal.classList.add('error');
            return;
        }
        const url = `/usuario/mi-cuenta/?email=${encodeURIComponent(inputModal.value)}`;
        validarCampoAjax(url, inputFeedback, "El email ingresado ya está registrado.", () => {
            document.getElementById("editForm").submit();
        });

    }     
    else if (campoSeleccionado === "password") {
        const passwordRegex = /^(?=.*[A-Za-zñÑ])(?=.*[A-ZñÑ])(?=.*\d)[A-Za-zñÑ\d._@#$%&*!?-]{6,}$/;  // La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -
        if(!passwordRegex.test(inputnewPassword.value)){
            inputFeedback.textContent = "La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -";
            inputModal.classList.add('error');   
            return;
        }
        const url = `/usuario/mi-cuenta/?oldPassword=${encodeURIComponent(inputModal.value)}&newPassword=${encodeURIComponent(inputnewPassword.value)}`;
        validarCampoAjax(url, inputFeedback, "La contraseña actual no coincide con la original.", () => {
            document.getElementById("editForm").submit();
        });

    }     
    else if(campoSeleccionado == "first_name" || campoSeleccionado == "last_name" ){
        const nombreRegex = /^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{1,}$/; 
        if(!nombreRegex.test(inputModal.value)){
            inputFeedback.textContent = "Este campo debe tener al menos 2 letras y solo contener letras.";
            inputModal.classList.add('error');   
            return;       
        }     
        const url = `/usuario/mi-cuenta/?nombre=${encodeURIComponent(inputModal.value)}`;
        validarCampoAjax(url, inputFeedback, "Este campo debe tener al menos 2 letras y solo contener letras.", () => {
            document.getElementById("editForm").submit();
        }); 
    } 
    else if (campoSeleccionado === "fecha_nacimiento") {
        const url = `/usuario/mi-cuenta/?fecha_nacimiento=${encodeURIComponent(inputModal.value)}`;
        validarCampoAjax(url, inputFeedback, "Debes tener al menos 18 años.", () => {
            document.getElementById("editForm").submit();
        });
    }      
    else if (campoSeleccionado === "cod_area") {
        const url = `/usuario/mi-cuenta/?cod_area=${encodeURIComponent(inputModal.value)}`;
        validarCampoAjax(url, inputFeedback, "El código de área seleccionado no es válido.", () => {
            document.getElementById("editForm").submit();
        });
    }
    else if (campoSeleccionado === "telefono") {
        const telefonoRegex =  /^[0-9]{6,8}$/; 
        if(!telefonoRegex.test(inputModal.value)){
            inputFeedback.textContent = "El número de teléfono debe contener entre 6 y 8 dígitos.";
            inputModal.classList.add('error');  
            return;       
        }
        const url = `/usuario/mi-cuenta/?telefono=${encodeURIComponent(inputModal.value)}`;
        validarCampoAjax(url, inputFeedback, "El número de teléfono debe contener entre 6 y 8 dígitos.", () => {
            document.getElementById("editForm").submit();
        });

    }      

});









