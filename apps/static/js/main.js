console.log('Hello World')

let charts_btn = document.getElementById('show-charts')
let charts_div = document.getElementById('chart')

charts_btn.addEventListener('click', toggleClass);
function toggleClass(){
  charts_div.classList.toggle('not-visible')
}
