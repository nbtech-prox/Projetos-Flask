function updateLabel() {
    var fileInput = document.getElementById('file');
    var label = document.querySelector('label[for="file"]'); 
    var fileName = fileInput.files[0].name;
    label.textContent = 'Ficheiro selecionado: ' + fileName;
}