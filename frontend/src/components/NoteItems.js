import React from 'react';

const NoteItem = ({ note }) => {
    return (
        <div className="note-item">
            <h3>{note.title}</h3>
            <p>{note.content}</p>
            <p>Created by: {note.author.username}</p>
            <p>Last modified: {new Date(note.timestamp).toLocaleString()}</p>
            <button onClick={() => deleteNote(note.id)}>Delete</button>
        </div>
    );
};

export default NoteItem;