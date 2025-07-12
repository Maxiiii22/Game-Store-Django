document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('menu-toggle');
    const navbar = document.getElementById('navbar');
    const openIcon = document.getElementById('open-icon');
    const closeIcon = document.getElementById('close-icon');
    const formBusqueda = document.getElementById('form-busqueda');
    const barraBusqueda = document.querySelector(".input-busqueda");
    const listaSugerencias = document.getElementById('sugerencia');
    const contenedorBusqueda = document.querySelector('.box-input-busqueda');


    const contenidoBarra = document.querySelector(".contenido-barra-noticias");
    const items = contenidoBarra.querySelectorAll("p");

    let currentItem = 0;

    // Función para mover el contenido
    function scrollContent() {
        // Desplazar el contenido hacia arriba, mostrando el siguiente mensaje
        contenidoBarra.style.transform = `translateY(-${currentItem * 18}px)`;  // Cada <p> tiene 18px de altura

        // Incrementar el índice para mostrar el siguiente item
        currentItem = (currentItem + 1) % items.length;  // Regresa al primer ítem después de mostrar todos
    }

    // Mostrar el primer mensaje inmediatamente al cargar la página
    contenidoBarra.style.transform = `translateY(0px)`;  // Empieza en la posición inicial

    // Configuramos que la animación se repita cada 10 segundos
    setInterval(scrollContent, 5000);  // Desplazar cada 5 segundos

    toggleBtn.addEventListener('click', () => {
        navbar.classList.toggle('active');

        if (navbar.classList.contains('active')) {
            openIcon.style.display = 'none';
            closeIcon.style.display = 'inline';
        } else {
            openIcon.style.display = 'inline';
            closeIcon.style.display = 'none';
        }
    });

    barraBusqueda.addEventListener("input", function () {
        let consulta = this.value;  // Obtener el texto del campo de búsqueda

        if (consulta.length > 2) {  // Solo hacer la búsqueda si hay más de 2 caracteres
          fetch(`/busqueda/?consulta=${consulta}`, {
            method: 'GET',
            headers: {
              'X-Requested-With': 'XMLHttpRequest',  // Aseguramos que el encabezado se envíe
              'Content-Type': 'application/json',    // Esto es solo para asegurarse de que el servidor lo maneje correctamente
            }
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Error al obtener las sugerencias');
              }
              return response.json();
            })
            .then(data => {
              if (data.error) {
                console.error(data.error);  // Si el servidor devuelve un error, lo mostramos
                return;
              }
      
              listaSugerencias.innerHTML = '';  // Limpiar las sugerencias anteriores
      
              data.forEach(sugerencia => {
                let li = document.createElement('li');
                li.textContent = sugerencia;
                // Agregar un evento click a cada sugerencia
                li.addEventListener('click', function () {
                    barraBusqueda.value = sugerencia;  // Coloca el valor en el input
                    listaSugerencias.innerHTML = '';  // Limpiar las sugerencias después de seleccionar una
                    formBusqueda.submit();
                });                
                listaSugerencias.appendChild(li);  // Agregar la sugerencia como un <li>
              });
            })
            .catch(error => {
              console.error('Hubo un problema con la solicitud:', error);
            });
        } else {
            listaSugerencias.innerHTML = '';  // Limpiar las sugerencias si no hay texto
        }  
    });

    document.addEventListener('click', function(event) {
        if (!contenedorBusqueda.contains(event.target)) {
            listaSugerencias.innerHTML = '';  
        }
    });

});