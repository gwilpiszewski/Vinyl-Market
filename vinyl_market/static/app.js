let trackform = document.querySelectorAll(".track-form");
let formcontainer = document.querySelector("#form-container");
let addformbutton = document.querySelector(`#add-form`);
let totalForms = document.querySelector("#form-TOTAL_FORMS");
let formNum = trackform.length-1;

addformbutton.addEventListener('click', addForm);

function addForm(e) {
    e.preventDefault()
    let newForm = trackform[0].cloneNode(true)
    let formRegex = RegExp(`form-(\\d){1}-`,'g')

    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    formcontainer.insertBefore(newForm, addformbutton)
    totalForms.setAttribute('value', `${formNum+1}`)


}

