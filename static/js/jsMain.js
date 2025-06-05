const personeriaButton = document.getElementById('personeria');
const contraloriaButton = document.getElementById('contraloria');
const contraloriaArticle = document.getElementById('comptroller');
const personeriaArticle = document.getElementById('ombudsman');

personeriaButton.addEventListener('click', function() { 
    contraloriaButton.classList.remove('d-none');
    personeriaButton.classList.add('d-none');
    personeriaArticle.classList.remove('d-none');
    personeriaArticle.classList.add('container', 'd-flex', 'flex-wrap', 'justify-content-around', 'mt-5');
    contraloriaArticle.classList.remove('container', 'd-flex', 'flex-wrap', 'justify-content-around', 'mt-5');
    contraloriaArticle.classList.add('d-none');
});
contraloriaButton.addEventListener('click', function() {
    personeriaButton.classList.remove('d-none');
    contraloriaButton.classList.add('d-none');
    contraloriaArticle.classList.remove('d-none');
    contraloriaArticle.classList.add('container', 'd-flex', 'flex-wrap', 'justify-content-around', 'mt-5');
    personeriaArticle.classList.remove('container', 'd-flex', 'flex-wrap', 'justify-content-around', 'mt-5');
    personeriaArticle.classList.add('d-none');
})
