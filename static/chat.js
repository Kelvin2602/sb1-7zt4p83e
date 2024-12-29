let currentUser = null;
let currentRoom = 'general';
const socket = io('http://localhost:8000');

// Kết nối và xác thực
async function initializeChat() {
    try {
        const response = await fetch('/api/auth/me');
        currentUser = await response.json();
        
        document.getElementById('userName').textContent = currentUser.full_name;
        document.getElementById('userRole').textContent = currentUser.role;
        if (currentUser.avatar_url) {
            document.getElementById('userAvatar').src = currentUser.avatar_url;
        }

        if (currentUser.role === 'admin') {
            document.getElementById('adminControls').style.display = 'block';
        }

        joinRoom('general');
        loadRooms();
    } catch (error) {
        console.error('Lỗi khởi tạo:', error);
    }
}

// Hiển thị tin nhắn
function displayMessage(message) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${message.sender_id === currentUser.id ? 'sent' : 'received'}`;
    messageDiv.setAttribute('data-message-id', message.id);
    
    messageDiv.innerHTML = `
        <img src="${message.sender_avatar || '/static/default-avatar.png'}" class="message-avatar" alt="Avatar">
        <div class="message-content">
            ${message.content}
            <div class="message-info">
                ${message.sender_name} • ${new Date(message.created_at).toLocaleTimeString()}
                <button class="delete-message" onclick="deleteMessage('${message.id}')">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Xóa tin nhắn
async function deleteMessage(messageId) {
    if (confirm('Bạn có chắc muốn xóa tin nhắn này?')) {
        try {
            await fetch(`/api/chat/messages/${messageId}`, {
                method: 'DELETE'
            });
            
            // Xóa tin nhắn khỏi giao diện
            const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
            if (messageElement) {
                messageElement.remove();
            }
            
            // Thông báo cho các client khác
            socket.emit('message_deleted', {
                messageId,
                roomId: currentRoom
            });
        } catch (error) {
            console.error('Lỗi khi xóa tin nhắn:', error);
            alert('Không thể xóa tin nhắn. Vui lòng thử lại sau.');
        }
    }
}

// Lắng nghe sự kiện xóa tin nhắn
socket.on('message_deleted', (data) => {
    const messageElement = document.querySelector(`[data-message-id="${data.messageId}"]`);
    if (messageElement) {
        messageElement.remove();
    }
});

// ... (giữ nguyên các hàm khác)