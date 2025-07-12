function clickImg(smallImg){
    var fullImg = document.getElementById("imagenbox");
    fullImg.src = smallImg.src;
}

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

function agregarAlCarrito(modelo, id) {
    fetch(`/carrito/agregar/${modelo}/${id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(res => {
        if (res.redirected) {
            // Si la respuesta fue una redirección (login), redirigimos al usuario
            window.location.href = res.url;  // Redirige al login o la página indicada
            return Promise.reject("Redirigido, no continuar");  // Rechazamos la promesa para evitar que pase al catch
        }

        if (res.ok) {
            return res.json();  // Si es una respuesta válida, la procesamos
        } else {
            return Promise.reject('Error en la solicitud');
        }
    })
    .then(data => {
        if (data.carrito_count !== undefined) {
            document.getElementById('carrito-count').innerText = data.carrito_count;
            Toastify({
                text: "Producto añadido 🛒",
                duration: 2000,
                gravity: "top",
                style: { background: "#4CAF50"},
                offset: {
                    x: 10,               // ligero desplazamiento desde el borde derecho
                    y: 70                // baja un poco para evitar topbars o headers
                },
                stopOnFocus: true        // permite pausar si el usuario pasa el mouse 
            }).showToast();
        }
        else{
            console.log("error")
        }
    })
    .catch(error => {
        if (error === "Redirigido, no continuar") {
            // Si la promesa fue rechazada debido a la redirección, no hacemos nada en el catch
            return;
        }

        console.error("Error en agregar al carrito:", error);
        Toastify({
            text: "Ocurrió un error. Intenta nuevamente",
            duration: 2000,
            gravity: "top",
            style: { background: "#f44336"},
            offset: { x: 10, y: 70 }
        }).showToast();
    });
}


document.addEventListener('DOMContentLoaded', () => {
    const marcas = document.querySelectorAll(".marca-producto");

    marcas.forEach(marca => {
        marca.addEventListener('click', function() {
            console.log("click")
            const marcaId = marca.getAttribute('data-marca-id');
            
            // Creamos la URL con el parámetro de marca
            const url = new URL(window.location.href);
            url.searchParams.set('marca', marcaId);  // Agregamos el filtro de marca

            // Redirigimos a la misma página con el filtro aplicado
            window.location.href = url.toString();
        });
    });

    document.querySelectorAll('#btn-agregar-carrito').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault() // Evita que el boton dentro del <a></a> siga el enlace
            e.stopPropagation(); // Detiene la propagacion del evento hacia el <a>
            agregarAlCarrito(btn.dataset.modelo, btn.dataset.id);
        });
    });
});


