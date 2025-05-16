import { useEffect, useState } from 'react';
import axios from 'axios';

export default function ExercisePage() {
  const [exercises, setExercises] = useState([]);

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (!userId) return;

    axios.get(`https://ortal.ngrok.io/get_exercises?user_id=${userId}`)
      .then(res => setExercises(res.data.exercises || []))
      .catch(err => console.error("Error loading exercises", err));
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>🧘 Saved Exercises</h2>
      {exercises.length === 0 ? (
        <p>No exercises yet. Ask the bot for some!</p>
      ) : (
        exercises.map((ex, i) => (
          <button key={i} style={{ display: 'block', margin: '10px 0' }}>
            {ex}
          </button>
        ))
      )}
    </div>
  );
}
