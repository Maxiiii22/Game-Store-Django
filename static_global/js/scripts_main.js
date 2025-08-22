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

    function scrollContent() {
        contenidoBarra.style.transform = `translateY(-${currentItem * 18}px)`;  

        currentItem = (currentItem + 1) % items.length;  
    }

    contenidoBarra.style.transform = `translateY(0px)`;  

    setInterval(scrollContent, 5000);  

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
        let consulta = this.value;  

        if (consulta.length > 2) { 
          fetch(`/busqueda/?consulta=${consulta}`, {
            method: 'GET',
            headers: {
              'X-Requested-With': 'XMLHttpRequest',  
              'Content-Type': 'application/json',   
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
                console.error(data.error); 
                return;
              }
      
              listaSugerencias.innerHTML = '';  
      
              data.forEach(sugerencia => {
                let li = document.createElement('li');
                li.textContent = sugerencia;
                li.addEventListener('click', function () {
                    barraBusqueda.value = sugerencia; 
                    listaSugerencias.innerHTML = '';  
                    formBusqueda.submit();
                });                
                listaSugerencias.appendChild(li);  
              });
            })
            .catch(error => {
              console.error('Hubo un problema con la solicitud:', error);
            });
        } else {
            listaSugerencias.innerHTML = '';  
        }  
    });

    document.addEventListener('click', function(event) {
        if (!contenedorBusqueda.contains(event.target)) {
            listaSugerencias.innerHTML = '';  
        }
    });

});
