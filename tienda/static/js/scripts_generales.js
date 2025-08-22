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
            window.location.href = res.url; 
            return Promise.reject("Redirigido, no continuar");  
        }

        if (res.ok) {
            return res.json();  
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
                    x: 10,               
                    y: 70              
                },
                stopOnFocus: true       
            }).showToast();
        }
        else{
            console.log("error")
        }
    })
    .catch(error => {
        if (error === "Redirigido, no continuar") {
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


