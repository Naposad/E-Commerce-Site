
document.addEventListener('DOMContentLoaded',()=>{
    const bmenu = document.querySelector('#cli');
    const bclose = document.querySelector('#close');

    bmenu.addEventListener('click', ()=>{
        bmenu.classList.toggle('open')
    })
})