document.addEventListener('DOMContentLoaded', function () {
    const configButton = document.getElementById('configuracion-color');
    const closeButton = document.getElementById('cerrar-ajuste');
    const saveButton = document.getElementById('guardar-cambios');
    const colorButtons = document.querySelectorAll('.color-choice');
    const modalElement = document.getElementById('settingsPanel');
    const modal = new bootstrap.Modal(modalElement);
    const className = 'btn-modificable';

    let selectedColor = localStorage.getItem('selectedColor') || '#ED1C24';

    // Aplicar el color inicial desde localStorage
    applyColor(selectedColor);

    // Mostrar el modal
    configButton.addEventListener('click', function () {
        modal.show();
    });

    // Cerrar el modal
    closeButton.addEventListener('click', function () {
        modal.hide();
    });

    // Seleccionar un color
    colorButtons.forEach(button => {
        button.addEventListener('click', function () {
            selectedColor = this.getAttribute('data-color');
            highlightSelectedButton(button);
        });
    });

    // Guardar los cambios
    saveButton.addEventListener('click', function () {
        localStorage.setItem('selectedColor', selectedColor);
        applyColor(selectedColor);
        modal.hide();
    });

    // Resalta el botón seleccionado
    function highlightSelectedButton(selectedButton) {
        colorButtons.forEach(button => button.style.border = 'none');
        selectedButton.style.border = '3px solid #000';
    }

    // Aplicar el color seleccionado a los botones
    function applyColor(color) {
        document.querySelectorAll(`.${className}`).forEach(button => {
            button.style.backgroundColor = color;
            button.style.borderColor = color;
            button.style.color = '#fff';
        });
    }
});
