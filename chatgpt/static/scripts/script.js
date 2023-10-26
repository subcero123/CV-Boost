const fileInput = document.getElementById("file-input");
const uplobutton = document.getElementById("acceptButton");

uplobutton.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        var formData = new FormData();
        formData.append("cv_file", file);

        fetch('/obtener_sugerencias', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const resultadoDiv = document.getElementById('resultado');
            resultadoDiv.innerHTML = ''; // Limpia el contenido anterior (si lo hubiera)

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
    }
});
