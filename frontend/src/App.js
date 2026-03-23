import React, { useEffect, useState } from 'react';

function App() {
  const [experiments, setExperiments] = useState([]);

  const fetchExperiments = () => {
    fetch("http://127.0.0.1:8000/experiments")
      .then(res => res.json())
      .then(data => setExperiments(data))
      .catch(err => console.error("Error:", err));
  };

  useEffect(() => { fetchExperiments(); }, []);

  // 1. 创建新实验
  const handleSubmit = () => {
    const name = document.getElementById('input-name').value;
    const hypo = document.getElementById('input-hypothesis').value;
    fetch("http://127.0.0.1:8000/experiments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, hypothesis: hypo, owner: "Juana Zhang" })
    }).then(() => { window.location.reload(); });
  };

  // 2. 核心自动化：直接在页面更新 A/B 测试结果
  const handleUpdateResults = (id) => {
    const c_conv = document.getElementById(`c_conv_${id}`).value;
    const c_user = document.getElementById(`c_user_${id}`).value;
    const v_conv = document.getElementById(`v_conv_${id}`).value;
    const v_user = document.getElementById(`v_user_${id}`).value;

    fetch(`http://127.0.0.1:8000/experiments/${id}/update-results?c_conversions=${c_conv}&c_users=${c_user}&v_conversions=${v_conv}&v_users=${v_user}`, {
      method: "POST"
    })
    .then(res => res.json())
    .then(data => {
      alert(`Analysis Complete! Significant: ${data.is_significant}`);
      fetchExperiments(); // 局部刷新数据，看到勋章跳出来
    });
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <h1 style={{ color: '#2c3e50' }}>🔬 ExperimentOS Dashboard</h1>
      
      {/* 注册区 */}
      <div style={{ marginBottom: '30px', background: '#fff', padding: '20px', borderRadius: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.05)' }}>
        <h3 style={{ marginTop: 0 }}>➕ Register New Experiment</h3>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input id="input-name" placeholder="Experiment Title" style={{ padding: '8px', flex: 1 }} />
          <input id="input-hypothesis" placeholder="Hypothesis" style={{ padding: '8px', flex: 2 }} />
          <button onClick={handleSubmit} style={{ padding: '8px 20px', backgroundColor: '#3498db', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Submit</button>
        </div>
      </div>

      {/* 实验卡片列表 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: '20px' }}>
        {experiments.map(exp => (
          <div key={exp.id} style={{ 
            background: '#fff', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 15px rgba(0,0,0,0.08)', 
            borderLeft: exp.is_significant ? '8px solid #27ae60' : '8px solid #3498db', position: 'relative' 
          }}>
            {exp.is_significant && <div style={{ position: 'absolute', top: '-10px', right: '-10px', backgroundColor: '#27ae60', color: '#fff', padding: '5px 12px', borderRadius: '20px', fontWeight: 'bold' }}>🏆 WINNER</div>}
            
            <h3>{exp.name}</h3>
            <p style={{ color: '#7f8c8d', fontSize: '0.9em' }}>{exp.hypothesis}</p>

            {/* 自动化录入区 */}
            <div style={{ backgroundColor: '#f9f9f9', padding: '15px', borderRadius: '8px', marginTop: '10px', border: '1px solid #eee' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '0.8em' }}>
                <div><strong>Control (Conv/Total)</strong><br/>
                  <input id={`c_conv_${exp.id}`} placeholder="Conv" style={{ width: '40px' }} /> / <input id={`c_user_${exp.id}`} placeholder="Total" style={{ width: '50px' }} />
                </div>
                <div><strong>Variant (Conv/Total)</strong><br/>
                  <input id={`v_conv_${exp.id}`} placeholder="Conv" style={{ width: '40px' }} /> / <input id={`v_user_${exp.id}`} placeholder="Total" style={{ width: '50px' }} />
                </div>
              </div>
              <button onClick={() => handleUpdateResults(exp.id)} style={{ width: '100%', marginTop: '10px', padding: '5px', backgroundColor: '#2c3e50', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                Run Statistical Analysis
              </button>
            </div>

            <div style={{ marginTop: '15px', fontSize: '0.85em', color: exp.is_significant ? '#27ae60' : '#7f8c8d' }}>
              <strong>P-value:</strong> {exp.p_value ?? 'N/A'} | <strong>Status:</strong> {exp.is_significant ? '✅ Significant' : exp.status}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;