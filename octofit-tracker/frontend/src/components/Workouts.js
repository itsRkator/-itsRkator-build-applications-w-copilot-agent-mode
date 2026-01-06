import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const codespace = process.env.REACT_APP_CODESPACE_NAME;
    const apiUrl = codespace 
      ? `https://${codespace}-8000.app.github.dev/api/workouts/`
      : 'http://localhost:8000/api/workouts/';
    
    console.log('Fetching from:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts data:', data);
        // Handle both paginated and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(workoutsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-5"><div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="alert alert-danger m-3">Error: {error}</div>;

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      'beginner': 'success',
      'intermediate': 'warning',
      'advanced': 'danger'
    };
    return badges[difficulty] || 'secondary';
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Workouts</h2>
      <div className="row">
        {workouts.map(workout => (
          <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">{workout.name}</h5>
                <p className="card-text">{workout.description}</p>
                <div className="mb-2">
                  <span className={`badge bg-${getDifficultyBadge(workout.difficulty)} me-2`}>
                    {workout.difficulty}
                  </span>
                  <span className="badge bg-info text-dark">
                    {workout.duration} min
                  </span>
                </div>
                <p className="card-text">
                  <small className="text-muted">Category: {workout.category}</small>
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Workouts;
