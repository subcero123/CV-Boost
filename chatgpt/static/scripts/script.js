const fileInput = document.getElementById("file-input");
const confirmButton = document.getElementById("confirm-button");
const uplobutton = document.getElementById("acceptButton");


// Agrega un escuchador de eventos al botón de subir archivo
uplobutton.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", () => {
    //Verifica que se haya seleccionado un archivo
    if (fileInput.files.length > 0) {
    const file = fileInput.files[0];
    var formData = new FormData();
    formData.append("cv_file", file);
    console.log(file);
    //Realiza una solicitud POST al endpoint
    }

    fetch('/obtener_sugerencias', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Muestra la respuesta en la página
            const resultadoDiv = document.getElementById('resultado');
            resultadoDiv.innerHTML = ''; // Limpia el contenido anterior (si lo hubiera)

            // Itera a través de las propiedades del objeto y muestra cada propiedad y su valor
            for (const propiedad in data) {
                if (data.hasOwnProperty(propiedad)) {
                    const parrafo = document.createElement('p');
                    parrafo.textContent = `${propiedad}: ${data[propiedad]}`;
                    resultadoDiv.appendChild(parrafo);
                }
            }
        })
        .catch(error => {
            console.error(error);
        });
});