import React, { useState, useEffect } from 'react';
import axios from 'axios';
import NoteItem from './NoteItems';

const NoteList = () => {
    const [notes, setNotes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchNotes = async () => {
        try {
            const response = await axios.get('/api/notes');
            setNotes(response.data);
        } catch (error) {
            console.error('Error fetching notes', error);
            setError('Failed to fetch notes');
        } finally {
            setLoading(false);
        }
    };

    const deleteNote = async (noteId) => {
        try {
          await axios.delete(`/api/notes/${noteId}`);
          fetchNotes();
        } catch (error) {
          setError('Error deleting note');
        }
      };
    

    useEffect(() => {
        fetchNotes();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>Notes</h1>
            <ul>
                {notes.map(note => (
                    <NoteItem key={note.id} note={note} deleteNote = {deleteNote} />
                ))}
            </ul>
        </div>
    );
};

export default NoteList;