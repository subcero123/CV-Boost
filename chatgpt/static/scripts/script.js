const fileInput = document.getElementById("file-input");
const confirmButton = document.getElementById("confirm-button");

    // Agrega un escuchador de eventos al botón de subir archivo
    uploadButton.addEventListener("click", () => {
        fileInput.click();
    });

    // Agrega un escuchador de eventos al input de archivo para manejar el cambio de archivo
    fileInput.addEventListener("change", () => {
        // Verifica que se haya seleccionado un archivo
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append("cv_file", file);

            // Realiza una solicitud POST al endpoint
            fetch('/obtener_sugerencias', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Muestra la respuesta en la página
                const suggestionsElement = document.createElement("div");
                suggestionsElement.innerHTML = `<p><strong>Sugerencias:</strong></p><p>${data}</p>`;
                document.body.appendChild(suggestionsElement);
            })
            .catch(error => {
                console.error(error);
            });
        }
    });