const metodoEnvioSelect = document.getElementById('metodo_envio');
const boxDireccion = document.getElementById('box-direccion');
const boxLocales = document.getElementById('box-locales');
const boxBoton = document.querySelector('.box-btn');
const infoIcons = document.querySelectorAll('.info-icon');
const inputsFormLocales = document.querySelectorAll('.inputs-form-local');
const inputsFormDirecciones = document.querySelectorAll('.inputs-form-direccion');

const inputDireccion = document.getElementById("id_direccion");
const inputNumeroPuerta = document.getElementById("id_numero_puerta");
const inputCiudad = document.getElementById("id_ciudad");
const inputProvincia = document.getElementById("id_provincia");
const inputCodPostal = document.getElementById("id_codigo_postal");
const inputInstruccionesEnvio = document.getElementById("id_instrucciones_envio");
const radiosTienda = document.querySelectorAll(".inputs-form-local"); 
const errorDireccion = document.getElementById("error-p-direccion");
const errorLocales = document.getElementById("error-p-locales");


function actualizarVistaMetodoEnvio() {
    const metodoEnvio = metodoEnvioSelect.value;
    
    // Mostrar u ocultar bloques según el valor seleccionado
    if (metodoEnvio === 'envio_estandar') {
        boxDireccion.classList.remove("hidden");
        boxLocales.classList.add("hidden");
        boxBoton.classList.remove("hidden");

        inputsFormDirecciones.forEach(input => {
            input.disabled = false;
        });

        inputsFormLocales.forEach(input => {
            input.disabled = true;
        });

    }   
    else if (metodoEnvio === 'retirar_tienda') {
        boxDireccion.classList.add("hidden");
        boxLocales.classList.remove("hidden");
        boxBoton.classList.remove("hidden");

        inputsFormDirecciones.forEach(input => {
            input.disabled = true;
        });

        inputsFormLocales.forEach(input => {
            input.disabled = false;
        });

    }
    else{
        boxDireccion.classList.add("hidden");
        boxLocales.classList.add("hidden");
        boxBoton.classList.add("hidden");

        inputsFormDirecciones.forEach(input => {
            input.disabled = true;
        });

        inputsFormLocales.forEach(input => {
            input.disabled = true;
        });
    }
}

// Ejecutar al cargar la página para asegurarse de que está bien inicialmente
window.onload = actualizarVistaMetodoEnvio;

// Ejecutar cada vez que el usuario cambie la opción del select
metodoEnvioSelect.addEventListener('change', actualizarVistaMetodoEnvio);

const botonConfirmar = document.getElementById('boton-confirmar-compra');
const spinner = document.getElementById('spinner');
const btnText = botonConfirmar.querySelector('.btn-text');

function activarCarga() {
    botonConfirmar.disabled = true;
    btnText.classList.add('hidden');     
    spinner.classList.remove('hidden');  
}

function desactivarCarga() {
    botonConfirmar.disabled = false;
    btnText.classList.remove('hidden'); 
    spinner.classList.add('hidden');    
}


// Verificamos si la clave pública está disponible
if (window.MERCADOPAGO_PUBLIC_KEY) {
    const mp = new MercadoPago(window.MERCADOPAGO_PUBLIC_KEY, {
        locale: 'es-AR',
    });

    const form = document.getElementById('form-confirmar-compra');

    form.addEventListener('submit', function(event) {
        errorDireccion.textContent = "";
        errorLocales.textContent = "";
        allCamposObligatorios = document.querySelectorAll("#metodo_envio, .input-box .campoMetodoEnvio, .tiendas-list .campoMetodoEnvio ")
        let hayErrores = false;
        let tiendasSeleccionada = false;
        event.preventDefault();

        if (!boxDireccion.classList.contains('hidden')){
            allCamposObligatorios.forEach(input => {
                if (!input.value.trim()) {
                    hayErrores = true;
                    input.setAttribute('required', true); 
                    input.classList.add('error');
                    let feedback = input.nextElementSibling;
                    if (!feedback || !feedback.classList.contains('campoFeedback')) {    // Verificar si ya existe un mensaje de error, para evitar duplicados
                        feedback = document.createElement('small');
                        feedback.classList.add('campoFeedback');
                        feedback.textContent = 'Este campo es obligatorio'; 
                        input.insertAdjacentElement('afterend', feedback);
                }
                }
            }); 
        }

        if (!boxLocales.classList.contains('hidden')){
            // Comprobamos si alguno de los radios está seleccionado
            radiosTienda.forEach(radio => {
                radio.setAttribute('required', true); 
                if (radio.checked) {
                    tiendasSeleccionada = true;
                }
            });
        
            if (!tiendasSeleccionada) {
                // Si no se seleccionó ninguna tienda, mostrar un mensaje de error
                errorLocales.innerText = "Debes seleccionar una tienda para el retiro."
                return;
            } 
        }

        if (hayErrores) {
        console.log("Hubo errores")
            return; 
        }

        const formData = new FormData(this);

        activarCarga();

        fetch("/carrito/confirmar-compra/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.preference_id) {
                renderMercadoPagoBrick(data.preference_id);
            } 
            else {
                console.log(data.error ||data.errorDireccion || data.errorLocales ||  "Error al crear la preferencia de pago");
                if(data.error){
                    errorDireccion.innerText = data.error || "Error al crear la preferencia de pago" + ",intentelo otra vez";
                    errorLocales.innerText = data.error || "Error al crear la preferencia de pago"+ ",intentelo otra vez";
                }
                else if(data.errorDireccion){
                    errorDireccion.innerText = data.errorDireccion;
                }
                else if(data.errorLocales){
                    errorLocales.innerText = data.errorLocales;
                }
                desactivarCarga();
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Hubo un problema al procesar tu compra.");
            desactivarCarga();
        });
    });

    // 🧹 Función para eliminar el brick de Mercado Pago si existe
    function removeWalletBrick() {
        const existingContainer = document.getElementById('walletBrick_container');
        if (existingContainer) {
            existingContainer.remove();
        }
        desactivarCarga();
    }

    // ⚙️ Función para renderizar el brick
    function renderMercadoPagoBrick(preference_id) {
        const bricksBuilder = mp.bricks();

        const renderWalletBrick = async () => {
            const formContainer = document.querySelector('.form-direccion');

            // Creamos el contenedor si no existe
            let walletContainer = document.getElementById('walletBrick_container');
            if (!walletContainer) {
                walletContainer = document.createElement('div');
                walletContainer.id = 'walletBrick_container';
                formContainer.appendChild(walletContainer);  
            }
            else {
                walletContainer.innerHTML = '';
            }

            try {
                await bricksBuilder.create("wallet", "walletBrick_container", {
                    initialization: {
                        preferenceId: preference_id,
                    },
                    configuration: {
                        theme: "light",
                        allowedPaymentMethods: ["credit_card", "debit_card"],
                        excludedPaymentTypes: ["ticket", "atm"],
                    },
                    callbacks: {
                        onReady: () => { // Cuando el brick carga completamente
                            btnText.classList.remove('hidden'); 
                            spinner.classList.add('hidden'); 
                        }
                    }
                });
            } catch (error) {
                console.error("Error al renderizar el brick de pago:", error);
            }
        };

        renderWalletBrick();
    }

    // 🎯 Escuchar cambios en todos los campos relevantes del formulario
    const inputsToWatch = form.querySelectorAll('input, select, textarea');
    inputsToWatch.forEach(input => {
        input.addEventListener('input', () => {
            removeWalletBrick();
        });

        input.addEventListener('change', () => { // si se cambia el valor del radioInput, select
            removeWalletBrick();
        });
    });

} 
else {
    console.error("No se encontró la clave pública de Mercado Pago.");
}


infoIcons.forEach(infoIcon => {
    infoIcon.addEventListener('click', function() {
        // Obtener el ID de la caja de información desde el atributo data-target
        const targetBoxId = infoIcon.getAttribute('data-target');
        const infoBox = document.getElementById(targetBoxId);

        // Alternar la visibilidad de la caja de información
        infoBox.classList.toggle('show');
        
        // Alternar la clase 'active' en el ícono (para cambiar el color)
        infoIcon.classList.toggle('active');
    });
});

// Cerrar la caja de información cuando el usuario haga clic fuera de ella
document.addEventListener('click', function(event) {
    // Verificar si el clic fue fuera de un ícono o caja de información
    infoIcons.forEach(infoIcon => {
        const targetBoxId = infoIcon.getAttribute('data-target');
        const infoBox = document.getElementById(targetBoxId);

        if (!infoBox.contains(event.target) && !infoIcon.contains(event.target)) {
            infoBox.classList.remove('show'); // Ocultar la caja
            infoIcon.classList.remove('active'); // Restablecer el color del ícono
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    if (metodoEnvioSelect) {
        metodoEnvioSelect.addEventListener("change", function () {
            metodoEnvioSelect.classList.remove('error');
            let feedback = metodoEnvioSelect.nextElementSibling;
            if(metodoEnvioSelect != ""){
                if (feedback && feedback.classList.contains('campoFeedback')) {
                    feedback.remove(); 
                }
            }
        });
    }

    // Validación para la Dirección
    if (inputDireccion) {
        inputDireccion.addEventListener("input", function () {
            let inputValue = this.value;
            this.value = inputValue.replace(/[^a-zA-Z0-9\s,#.-]/g, "");   // Permite letras, números, espacios, comas, puntos, guiones y #
            inputDireccion.classList.remove('error');
            let feedback = inputDireccion.nextElementSibling;
            if (feedback && feedback.classList.contains('campoFeedback')) {
                feedback.remove(); 
            }
        });
    }

    // Validación para el Número de puerta
    if (inputNumeroPuerta) {
        inputNumeroPuerta.addEventListener("input", function () {
            let inputValue = this.value;
            this.value = inputValue.replace(/[^a-zA-Z0-9\s]/g, ""); // Permite letras, números y espacios
            inputNumeroPuerta.classList.remove('error');
            let feedback = inputNumeroPuerta.nextElementSibling;
            if (feedback && feedback.classList.contains('campoFeedback')) {
                feedback.remove(); 
            }
        });
    }

    // Validación para la Ciudad
    if (inputCiudad) {
        inputCiudad.addEventListener("input", function () {
            let inputValue = this.value;
            this.value = inputValue.replace(/[^a-zA-Z\sáéíóúÁÉÍÓÚ]/g, "");   // Permite solo letras, espacios y tildes
            inputCiudad.classList.remove('error');
            let feedback = inputCiudad.nextElementSibling;
            if (feedback && feedback.classList.contains('campoFeedback')) {
                feedback.remove(); 
            }
        });
    }

    // Validación para la Provincia
    if (inputProvincia) {
        inputProvincia.addEventListener("change", function () {
            inputProvincia.classList.remove('error');
            let feedback = inputProvincia.nextElementSibling;
            if(inputProvincia != ""){
                if (feedback && feedback.classList.contains('campoFeedback')) {
                    feedback.remove(); 
                }
            }
        });
    }

    // Validación para el Código Postal
    if (inputCodPostal) {
        inputCodPostal.addEventListener("keypress", function (event) {
            let inputValue = this.value + event.key; // Añadimos el carácter que intenta escribir
            inputCodPostal.classList.remove('error');
            let feedback = inputCodPostal.nextElementSibling;
            if (feedback && feedback.classList.contains('campoFeedback')) {
                feedback.remove(); 
            }
    
            // Eliminar caracteres no alfanuméricos
            if (/[^a-zA-Z0-9]/.test(event.key)) {
                event.preventDefault(); // Impide que se ingrese un carácter no válido
                return;
            }
    
            // Verificamos si el primer carácter es un número o una letra
            if (/^\d/.test(inputValue)) {
                // Si empieza con un número, debe ser un código postal numérico (4 dígitos)
                if (inputValue.length > 4) {
                    event.preventDefault(); // Impide que se ingrese más de 4 dígitos numéricos
                }
            } else if (/^[A-Za-z]/.test(inputValue)) {
                // Si empieza con una letra, debe ser un código postal alfanumérico (1 letra + 4 dígitos + 2-3 letras)
                if (inputValue.length > 8) {
                    event.preventDefault(); // Impide que se ingrese más de 8 caracteres alfanuméricos
                }
            }
    
            // Si el valor no es válido según el patrón, no permitimos la tecla
            if (inputValue.length >= 9) {
                event.preventDefault(); // Si el código postal es mayor a 8 caracteres, no permitimos más
            }
        });
    
        // Recortar caracteres no alfanuméricos y asegurar longitud correcta
        inputCodPostal.addEventListener("input", function () {
            let inputValue = this.value;
    
            // Eliminar caracteres no alfanuméricos
            inputValue = inputValue.replace(/[^a-zA-Z0-9]/g, "");
            this.value = inputValue;
    
            // Recorte para códigos postales numéricos (solo 4 dígitos)
            if (/^\d{4}$/.test(inputValue) && inputValue.length > 4) {
                this.value = inputValue.slice(0, 4);
            }
            // Recorte para códigos postales alfanuméricos (1 letra + 4 dígitos + 2-3 letras)
            else if (/^[A-Za-z]{1}\d{4}[A-Za-z]{2,3}$/.test(inputValue) && inputValue.length > 8) {
                this.value = inputValue.slice(0, 8);
            }
        });
    }

    if (inputInstruccionesEnvio) {
        inputInstruccionesEnvio.addEventListener("input", function () {
            let inputValue = this.value;
            if (inputValue.length > 500) {  
                this.value = inputValue.slice(0, 500);  // Limita a 500 caracteres
            }
        });
    }

    radiosTienda.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                errorLocales.innerText = ""
                console.log("Tienda seleccionada:", this.value);
            }
        });
    });


});


