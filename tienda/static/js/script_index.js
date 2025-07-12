
document.addEventListener('DOMContentLoaded', () => {
  const barraBusqueda = document.querySelector(".input-busqueda");

  const carrusel_juegos = document.getElementById('juegos-carrusel');
  const cards_juegos = carrusel_juegos.querySelectorAll('.card-juego');
  const btnAnterior_juegos = document.getElementById('juegos-anterior');
  const btnSiguiente_juegos = document.getElementById('juegos-siguiente');

  const carrusel_celus = document.getElementById('celulares-carrusel');
  const cards_celus = carrusel_celus.querySelectorAll('.card-celu');
  const btnAnterior_celus = document.getElementById('celulares-anterior');
  const btnSiguiente_celus = document.getElementById('celulares-siguiente');  

  // carrusel todos los productos:
  const lista = document.querySelector(".container-productos .carrusel-productos");
  const puntos = document.querySelectorAll(".carrusel-productos-btns .puntos li");
  const btnAnterior_productos = document.getElementById("anterior");
  const btnSiguiente_productos = document.getElementById("siguiente");
  let items = document.querySelectorAll(".container-productos .carrusel-productos .carrusel-productos-items");

  
  let active = 0 ;
  let lengthItems = items.length - 1;  



  const updateVisibleCount = () => {
    const width = window.innerWidth;
    if (width <= 768) visibleCount = 2;
    else if (width <= 1024) visibleCount = 3;
    else visibleCount = 5;
  };

  let currentIndexJuegos = 0;
  let currentIndexCelulares = 0;
  let visibleCount = 5;

  const updateCarrusel = (carrusel, card) => {
    if(carrusel === carrusel_juegos){
      const cardWidth = carrusel.querySelector('.card-juego').offsetWidth + 20; // 20px del gap
      const maxIndex = Math.max(0, card.length - visibleCount);
      currentIndexJuegos = Math.min(currentIndexJuegos, maxIndex);
      const offset = -(cardWidth * currentIndexJuegos);
      carrusel.style.transform = `translateX(${offset}px)`;
    }
    else if(carrusel === carrusel_celus){
      const cardWidth = carrusel.querySelector('.card-celu').offsetWidth + 20;
      const maxIndex = Math.max(0, card.length - visibleCount);
      currentIndexCelulares = Math.min(currentIndexCelulares, maxIndex);
      const offset = -(cardWidth * currentIndexCelulares);
      carrusel.style.transform = `translateX(${offset}px)`;
    }

  };

  btnAnterior_juegos.addEventListener('click', () => {
    if (currentIndexJuegos > 0) {
      currentIndexJuegos--;
      updateCarrusel(carrusel_juegos,cards_juegos);
    }
  });

  btnSiguiente_juegos.addEventListener('click', () => {
    const maxIndex = Math.max(0, cards_juegos.length - visibleCount);
    if (currentIndexJuegos < maxIndex) {
      currentIndexJuegos++;
      updateCarrusel(carrusel_juegos,cards_juegos);
    }
  });

  btnAnterior_celus.addEventListener('click', () => {
    if (currentIndexCelulares > 0) {
      currentIndexCelulares--;
      updateCarrusel(carrusel_celus,cards_celus);
      console.log("btnanterior")
    }
  });

  btnSiguiente_celus.addEventListener('click', () => {
    const maxIndex = Math.max(0, cards_celus.length - visibleCount);
    if (currentIndexCelulares < maxIndex) {
      currentIndexCelulares++;
      updateCarrusel(carrusel_celus,cards_celus);
      console.log("btnsiguiente")
    }
  });

  window.addEventListener('resize', () => {
    updateVisibleCount();
    updateCarrusel(carrusel_juegos,cards_juegos);
    updateCarrusel(carrusel_celus,cards_celus);
  });

  updateVisibleCount();
  updateCarrusel(carrusel_juegos,cards_juegos);
  updateCarrusel(carrusel_celus,cards_celus);


  btnSiguiente_productos.onclick = function(){
    if(active + 1 > lengthItems){
      active = 0;
    }
    else{
      active = active + 1;
    }
    reloadSlider();
  }
  
  btnAnterior_productos.onclick = function(){
    if(active - 1 < 0){
      active = lengthItems;
    }
    else{
      active = active - 1;
    }
    reloadSlider();
  }
  
  let refreshSlider = setInterval(() => {siguiente.click()}, 10000);

  barraBusqueda.addEventListener("focus", () => {
    clearInterval(refreshSlider);
  });

  barraBusqueda.addEventListener("blur", () => {
      refreshSlider = setInterval(() => { btnSiguiente_productos.click(); }, 10000);
  });
  
  function reloadSlider(){
    let checkLeft = items[active].offsetLeft;
    lista.style.left = -checkLeft + "px";
  
    let lastActivePunto = document.querySelector(".carrusel-productos-btns .puntos li.active");
    lastActivePunto.classList.remove("active")
    puntos[active].classList.add("active")
  }
  
  puntos.forEach((li,key) => {
    li.addEventListener("click", function(){
      active = key;
      reloadSlider();
    })
  })


});





