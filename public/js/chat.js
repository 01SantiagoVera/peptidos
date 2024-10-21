document.getElementById('chat-form').onsubmit = function(event) {
    event.preventDefault();

    // Obtener el valor del input
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value;

    // Crear un nuevo mensaje en el chat
    const chatBox = document.getElementById('chat-box');
    const newMessage = document.createElement('div');
    newMessage.classList.add('message', 'my-2', 'p-2', 'bg-light', 'text-dark', 'rounded');
    newMessage.innerHTML = `<strong>User:</strong> ${message}`;
    chatBox.appendChild(newMessage);

    // Limpiar el input
    chatInput.value = '';

    // Scroll hacia el final del chat
    chatBox.scrollTop = chatBox.scrollHeight;
};
