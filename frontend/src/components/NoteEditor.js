import React, { useState } from 'react';
import axios from 'axios';

const NoteEditor = ({ refreshNotes }) => {
  const [title, setTitle] = useState(note ? note.title : '');
  const [content, setContent] = useState(note ? note.content : '');
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (note) {
      setTitle(note.title);
      setContent(note.content);
    }
  }, [note]);

  const saveNoteLocally = (note) => {
    const localNotes = JSON.parse(localStorage.getItem('notes')) || [];
    localNotes.push(note);
    localStorage.setItem('notes', JSON.stringify(localNotes));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const noteData = { title, content };

    if (navigator.onLine) {
      try {
        if (note) {
          await axios.put(`/api/notes/${note.id}`, noteData);
        } else {
          await axios.post('/api/notes', noteData);
        }
        refreshNotes();
      } catch (error) {
        console.error('Error saving note:', error);
        setMessage('Error saving note. Please try again.');
      }
    } else {
      saveNoteLocally(noteData);
    }
  };

  return (
    <div className="card my-4">
      <div className="card-header bg-primary text-white">Add a New Note</div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Title</label>
            <input
              type="text"
              className="form-control"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Content</label>
            <textarea
              className="form-control"
              rows="3"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            ></textarea>
          </div>
          <button type="submit" className="btn btn-success">
            Save Note
          </button>
        </form>
        {message && <p>{message}</p>}
      </div>
    </div>
  );
};

export default NoteEditor;
