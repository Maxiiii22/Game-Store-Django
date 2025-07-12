function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.split('=')[1]);
                break;
            }
        }
    }
    return cookieValue;
}

function formatoMiles(valor) {
    return new Intl.NumberFormat('es-ES').format(valor);  // Le doy formato de miles en español al valor
}

function vaciarCarrito() {
    fetch("/carrito/vaciar-carrito/", {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();  
        }
        Toastify({
            text: "Se vacio el carrito",
            duration: 2000,
            gravity: "top",
            position: "right",
            style: { background: bgColor},
            offset: {
                x: 10,               // ligero desplazamiento desde el borde derecho
                y: 70                // baja un poco para evitar topbars o headers
            },
            stopOnFocus: true        // permite pausar si el usuario pasa el mouse                
        }).showToast();                  
    });
}


function actualizarLineaCarrito(modelo, id, accion) {
    fetch(`/carrito/${accion}/${modelo}/${id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const linea = document.querySelector(`button[data-id="${id}"]`).closest('.linea-producto');
            if (data.cantidad > 0) {
                // Actualizar cantidad y subtotal data.cantidad
                linea.querySelector('.cantidad').textContent = data.cantidad;
                linea.querySelector('.subtotal').textContent = `$${formatoMiles(data.subtotal)}`;
            } else {
                // Eliminar línea si la cantidad llegó a 0
                linea.remove();

                // Verificar si ya no quedan líneas
                const lineasRestantes = document.querySelectorAll('.linea-producto');
                if (lineasRestantes.length === 0) {
                    location.reload();  
                }
            }

            // Actualizar total y contador en navbar
            document.getElementById('total').textContent = `$${formatoMiles(data.total)}`;
            document.getElementById('carrito-count').textContent = data.carrito_count;

            // ✅ TOASTS según la acción
            let toastText = "";
            let bgColor = "";

            if (accion === "agregar") {
                toastText = "Cantidad aumentada ➕";
                bgColor = "#4CAF50";
            } else if (accion === "disminuir") {
                toastText = "Cantidad reducida ➖";
                bgColor = "#F44336";
            } else if (accion === "eliminar") {
                toastText = "Producto eliminado ❌";
                bgColor = "#C62828";
            }

            Toastify({
                text: toastText,
                duration: 2000,
                gravity: "top",
                position: "right",
                style: { background: bgColor},
                offset: {
                    x: 10,               // ligero desplazamiento desde el borde derecho
                    y: 70                // baja un poco para evitar topbars o headers
                },
                stopOnFocus: true        // permite pausar si el usuario pasa el mouse                
            }).showToast();                  
        }
        else{
            // Si no es exitoso (es decir, ocurrió un error como superar el precio máximo)
            Toastify({
                text: data.error || "Error desconocido. Intenta nuevamente.",
                duration: 3000,
                gravity: "top",
                position: "right",
                style: { background: "#E53935" }, 
                offset: {
                    x: 10,              
                    y: 70                
                },
                stopOnFocus: true                      
            }).showToast();            
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-agregar').forEach(btn => {
        btn.addEventListener('click', () => {
            actualizarLineaCarrito(btn.dataset.modelo, btn.dataset.id, 'agregar');
        });
    });

    document.querySelectorAll('.btn-menos').forEach(btn => {
        btn.addEventListener('click', () => {
            actualizarLineaCarrito(btn.dataset.modelo, btn.dataset.id, 'disminuir');
        });
    });

    document.querySelectorAll('.btn-eliminar').forEach(btn => {
        btn.addEventListener('click', () => {
            actualizarLineaCarrito(btn.dataset.modelo, btn.dataset.id, 'eliminar');
        });
    });

    document.querySelectorAll('.vaciar-carrito').forEach(btn => {
        btn.addEventListener('click', () => {
            vaciarCarrito()
        });
    });   
    
});

function togglePedido(id) {
    const boxPedido = document.getElementById("boxPedido-" + id);
    const div = document.getElementById("pedido-" + id);
    const openIcon = document.getElementById("open-pedidos-" + id);
    const closeIcon = document.getElementById("close-pedidos-" + id);

    const estaOculto = div.classList.contains("hidden-linea");

    if (estaOculto) {
        boxPedido.classList.add("visible-box");
        div.classList.remove("hidden-linea");
        div.classList.add("visible-linea");
        openIcon.classList.add("hidden");
        openIcon.classList.remove("visible");
        closeIcon.classList.add("visible");
        closeIcon.classList.remove("hidden");
    } 
    else {
        boxPedido.classList.remove("visible-box");
        div.classList.add("hidden-linea");
        div.classList.remove("visible-linea");
        openIcon.classList.add("visible");
        openIcon.classList.remove("hidden");
        closeIcon.classList.add("hidden");
        closeIcon.classList.remove("visible");
    }
}
