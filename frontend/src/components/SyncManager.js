import { useEffect, useState, useCallback } from 'react';
import axios from 'axios';

const SyncManager = () => {
    const [isOnline, setIsOnline] = useState(navigator.onLine);

    const syncNotes = useCallback(async () => {
        try {
            const response = await axios.get('/api/sync');
            console.log(response.data);
        } catch (error) {
            console.error('Error syncing notes:', error);
        }
    }, [refreshNotes]);

    useEffect(() => {
        const handleOnline = () => {
            setIsOnline(true);
            syncNotes();
        };

        const handleOffline = () => {
            setIsOnline(false);
        };

        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);

        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, [syncNotes]);

    useEffect(() => {
        if (isOnline) {
          const interval = setInterval(syncNotes, 60000); // Sync every 60 seconds
          return () => clearInterval(interval);
        }
      }, [isOnline, syncNotes]);
      return null;
};

export default SyncManager;