import React, { useEffect, useState } from 'react';

function App() {
  const [experiments, setExperiments] = useState([]);

  // 1. 自动获取实验列表
  useEffect(() => {
    fetch("http://127.0.0.1:8000/experiments")
      .then(res => res.json())
      .then(data => setExperiments(data))
      .catch(err => console.error("Error fetching data:", err));
  }, []);

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif', backgroundColor: '#f4f7f6', minHeight: '100vh' }}>
      <h1 style={{ color: '#2c3e50' }}>🔬 ExperimentOS Dashboard</h1>
      <p>Total Experiments: {experiments.length}</p>

      {/* 2. 创建实验表单区域 */}
      <div style={{ marginBottom: '30px', background: '#fff', padding: '20px', borderRadius: '12px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
        <h3 style={{ marginTop: 0 }}>➕ Create New Experiment</h3>
        <input id="new-name" placeholder="Experiment Name" style={{ padding: '8px', marginRight: '10px', borderRadius: '4px', border: '1px solid #ccc' }} />
        <input id="new-hypo" placeholder="Hypothesis" style={{ padding: '8px', marginRight: '10px', borderRadius: '4px', border: '1px solid #ccc', width: '300px' }} />
        <button 
          style={{ padding: '8px 16px', backgroundColor: '#3498db', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          onClick={() => {
            const name = document.getElementById('new-name').value;
            const hypo = document.getElementById('new-hypo').value;
            
            fetch("http://127.0.0.1:8000/experiments", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ name: name, hypothesis: hypo, owner: "Juana Zhang" })
            }).then(() => window.location.reload()); 
          }}
        >
          Submit
        </button>
      </div>

      {/* 3. 实验卡片展示区域 */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {experiments.map(exp => (
          <div key={exp.id} style={{ background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
            <h3 style={{ margin: '0 0 10px 0', color: '#3498db' }}>{exp.name}</h3>
            <p><strong>Hypothesis:</strong> {exp.hypothesis}</p>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '15px', fontSize: '0.9em' }}>
              <span>👤 {exp.owner}</span>
              <span style={{ 
                background: exp.status === 'Draft' ? '#bdc3c7' : '#27ae60', 
                color: 'white', 
                padding: '2px 8px', 
                borderRadius: '4px' 
              }}>
                {exp.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
} // <--- 确保这个大括号存在且在 export 前面

export default App;