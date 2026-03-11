import React, { useEffect, useState } from 'react';

function App() {
  const [experiments, setExperiments] = useState([]);

  // 1. Fetch experiment list from the backend
  useEffect(() => {
    fetch("http://127.0.0.1:8000/experiments")
      .then(res => res.json())
      .then(data => setExperiments(data))
      .catch(err => console.error("Error fetching data:", err));
  }, []);

  // 2. Handler to submit a new experiment
  const handleSubmit = () => {
    const nameValue = document.getElementById('input-name').value;
    const hypothesisValue = document.getElementById('input-hypothesis').value;

    fetch("http://127.0.0.1:8000/experiments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        name: nameValue, 
        hypothesis: hypothesisValue, 
        owner: "Juana Zhang",
        sample_size: 1000,      // Default value for Week 4
        conversion_rate: 0.05   // Default value for Week 4
      })
    })
    .then(res => {
      if (res.ok) {
        window.location.reload(); 
      } else {
        alert("Submission failed. Please check if the backend is running.");
      }
    })
    .catch(err => console.error("Submission Error:", err));
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <h1 style={{ color: '#2c3e50' }}>🔬 ExperimentOS Dashboard</h1>
      <p>Total Experiments Managed: <strong>{experiments.length}</strong></p>

      {/* Create Experiment Section */}
      <div style={{ marginBottom: '30px', background: '#fff', padding: '25px', borderRadius: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.05)' }}>
        <h3 style={{ marginTop: 0 }}>➕ Register New Experiment</h3>
        <div style={{ display: 'flex', gap: '15px' }}>
          <input id="input-name" placeholder="Experiment Title" style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ddd', flex: 1 }} />
          <input id="input-hypothesis" placeholder="Scientific Hypothesis" style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ddd', flex: 2 }} />
          <button 
            onClick={handleSubmit}
            style={{ padding: '10px 25px', backgroundColor: '#3498db', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Submit to Database
          </button>
        </div>
      </div>

      {/* Experiment Gallery */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '25px' }}>
        {experiments.map(exp => (
          <div key={exp.id} style={{ background: '#fff', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 15px rgba(0,0,0,0.08)', borderLeft: '5px solid #3498db' }}>
            <h3 style={{ margin: '0 0 12px 0', color: '#2c3e50' }}>{exp.name}</h3>
            <p style={{ fontSize: '0.95em', color: '#7f8c8d' }}><strong>Hypothesis:</strong> {exp.hypothesis}</p>
            <hr style={{ border: '0.5px solid #eee', margin: '15px 0' }} />
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85em' }}>
              <span>👤 <strong>Owner:</strong> {exp.owner}</span>
              <span style={{ 
                background: exp.status === 'Draft' ? '#ecf0f1' : '#27ae60', 
                color: exp.status === 'Draft' ? '#7f8c8d' : '#fff', 
                padding: '4px 12px', 
                borderRadius: '20px',
                fontWeight: 'bold'
              }}>
                {exp.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;