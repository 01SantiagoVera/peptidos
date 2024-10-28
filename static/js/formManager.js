document.getElementById("prediction-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Evita el envío del formulario de manera tradicional

    // Obtén el valor de la secuencia
    const sequence = document.querySelector('input[name="sequence"]').value;

    // Obtener la IP del usuario (considera capturarla desde el backend)
    const userIp = "192.168.1.1"; // Cambia esto por la IP real si es necesario

    // Realizar la solicitud POST
   fetch("/api/predict", { // Cambia esto si usas un prefijo
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ sequence: sequence, user_ip: userIp })
})

    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok'); // Manejo de errores de red
        }
        return response.json();
    })
    .then(data => {
        // Maneja la respuesta
        console.log("Respuesta del servidor:", data);
        alert("Predicción: " + data.prediction); // Muestra la predicción
    })
    .catch((error) => {
        console.error("Error:", error); // Muestra el error en consola
    });
});
