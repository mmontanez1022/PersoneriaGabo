// Obtiene el botón para mostrar Personería
const personeriaButton = document.getElementById('personeria');

// Obtiene el botón para mostrar Contraloría
const contraloriaButton = document.getElementById('contraloria');

// Obtiene la sección/artículo de Contraloría
const contraloriaArticle = document.getElementById('comptroller');

// Obtiene la sección/artículo de Personería
const personeriaArticle = document.getElementById('ombudsman');

// Evento cuando se hace click en el botón de Personería
personeriaButton.addEventListener('click', function() { 
    // Muestra el botón de Contraloría
    contraloriaButton.classList.remove('d-none');
    // Oculta el botón de Personería
    personeriaButton.classList.add('d-none');

    // Muestra la sección de Personería y le da estilos de Bootstrap
    personeriaArticle.classList.remove('d-none');
    personeriaArticle.classList.add('container', 'd-flex', 'flex-wrap', 'justify-content-around', 'mt-5');

    // Quita los estilos de la sección de Contraloría y la oculta
    contraloriaArticle.classList.remove('container', 'd-flex', 'flex-wrap', 'justify-content-around', 'mt-5');
    contraloriaArticle.classList.add('d-none');
});

// Evento cuando se hace click en el botón de Contraloría
contraloriaButton.addEventListener('click', function() {
    // Muestra el botón de Personería
    personeriaButton.classList.remove('d-none');
    // Oculta el botón de Contraloría
    contraloriaButton.classList.add('d-none');

    // Muestra la sección de Contraloría con estilos de Bootstrap
    contraloriaArticle.classList.remove('d-none');
    contraloriaArticle.classList.add('container', 'd-flex', 'flex-wrap', 'justify-content-around', 'mt-5');

    // Quita los estilos de Personería y la oculta
    personeriaArticle.classList.remove('container', 'd-flex', 'flex-wrap', 'justify-content-around', 'mt-5');
    personeriaArticle.classList.add('d-none');
});

