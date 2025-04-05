const socket = io();

// Unirse al chat con tu ID de usuario
const userId = "TU_ID"; // Debes obtenerlo dinámicamente
socket.emit('join', userId);

// Obtener el ID del receptor desde la URL (ejemplo: chat.html?receiverId=123)
const urlParams = new URLSearchParams(window.location.search);
const receiverId = urlParams.get('receiverId');

// Enviar mensaje
function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    if (message) {
        socket.emit('sendMessage', { senderId: userId, receiverId, message });
        addMessageToChat('Tú', message); // Mostrar tu mensaje localmente
        messageInput.value = '';
    }
}

// Recibir mensaje
socket.on('newMessage', (data) => {
    addMessageToChat(data.senderId, data.message);
    checkNewMessages(); // Actualizar el ícono de mensaje
});

// Mostrar mensajes en la interfaz
function addMessageToChat(sender, message) {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<p><strong>${sender}:</strong> ${message}</p>`;
}