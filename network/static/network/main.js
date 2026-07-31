function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : '';
}

function toggleLike(id) {
    fetch(`/like/${id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const likesElement = document.getElementById(`likes-${id}`);
        if (likesElement) {
            likesElement.innerText = data.likes;
        }
    });
}

function editPost(id) {
    const contentDiv = document.getElementById(`content-${id}`);
    if (!contentDiv) return;

    const oldContent = contentDiv.innerText;
    contentDiv.innerHTML = `
        <textarea id="edit-${id}" class="form-control">${oldContent}</textarea>
        <button class="btn btn-sm btn-success mt-2" onclick="savePost(${id})">Save</button>
    `;
}

function savePost(id) {
    const contentInput = document.getElementById(`edit-${id}`);
    if (!contentInput) return;

    const newContent = contentInput.value;

    fetch(`/edit/${id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ content: newContent })
    })
    .then(response => response.json())
    .then(data => {
        const contentElement = document.getElementById(`content-${id}`);
        if (contentElement) {
            contentElement.innerText = data.content;
        }
    });
}
