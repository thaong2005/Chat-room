function checkMessages() {
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');
    const msg = urlParams.get('msg');
    const statusBox = document.getElementById('status-message');

    if (!statusBox) return; // Safety check

    if (error) {
        statusBox.textContent = decodeURIComponent(error);
        statusBox.className = 'status-msg error'; // Ensure class is added
        statusBox.style.display = 'block';
    } else if (msg) {
        statusBox.textContent = decodeURIComponent(msg);
        statusBox.className = 'status-msg success';
        statusBox.style.display = 'block';
    }
}

checkMessages();