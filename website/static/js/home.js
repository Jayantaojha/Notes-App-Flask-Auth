const noteInput = document.querySelector('#note-input');
const logoutBtn = document.querySelector('.logout-btn');

logoutBtn.addEventListener('click', () => {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // Add CSRF token if your app uses CSRF protection
        credentials: 'include' // To include cookies in the request
    })
    .then(response => {
        if (response.redirected) {
            // If the server redirects after logout, follow the redirect
            window.location.href = response.url;
        } else {
            console.log('Logout successful, but no redirect');
        }
    })
    .catch(error => {
        console.error('Error during logout:', error);
    });
});


noteInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        const noteText = e.target.value.trim();
        if (noteText !== '') {
            fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ note: noteText })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Create a new list item for the note
                    const newNoteItem = document.createElement('li');
                    newNoteItem.className = 'note';
                    newNoteItem.innerHTML = `
                        <span class="note-text">${noteText}</span>
                        <div class="note-actions">
                            <button class="edit-btn" onclick="updateNote()">Edit</button>
                            <button class="delete-btn" onclick="deleteNote()">Delete</button>
                        </div>
                    `;

                    // Insert the new note at the top of the list
                    const notesList = document.getElementById('notes-list');
                    notesList.insertBefore(newNoteItem, notesList.firstChild);

                    // Clear the input field
                    e.target.value = '';
                } else {
                    console.error('Failed to add note:', data.message);
                }
            })
            .catch(error => {
                console.error('Error adding note:', error);
            });
        }
    }
});


function deleteNote(noteId){
    const noteElement = getNoteElement(noteId);

    fetch('/delete-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ noteid: noteId})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){
            noteElement.remove();
        }
        else{
            console.error("Failed to delete note: ", data.message);
        }
    })
    .catch(error => {
        console.error("Error deleting note: ", error);
    })
    
}


function updateNote(noteId){
    console.log("Update operation is called, Note Id: ", noteId);
    
}


function getNoteElement(noteId) {
    return document.querySelector(`.note-actions button[onclick*="'${noteId}'"]`).closest('li');
}
