import React, { useEffect, useState } from 'react';

// 确保这里的地址和后端一致
const API_BASE = "http://localhost:8000";

function App() {
  const [experiments, setExperiments] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // 拉取数据的函数
  const fetchExperiments = () => {
    setIsLoading(true);
    setError(null);
    
    fetch(`${API_BASE}/experiments`)
      .then(res => {
        if (!res.ok) throw new Error(`Status: ${res.status}`);
        return res.json();
      })
      .then(data => {
        setExperiments(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error("Error:", err);
        setError(`Failed to fetch experiments: ${err.message}`);
        setIsLoading(false);
      });
  };

  useEffect(() => { fetchExperiments(); }, []);

  // 1. 创建新实验
  const handleSubmit = () => {
    const name = document.getElementById('input-name').value;
    const hypo = document.getElementById('input-hypothesis').value;
    if (!name) return alert("Please enter a name");

    setIsLoading(true);
    fetch(`${API_BASE}/experiments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, hypothesis: hypo, owner: "Juana Zhang" })
    })
    .then(res => {
      if (!res.ok) throw new Error(`Status: ${res.status}`);
      return res.json();
    })
    .then(() => {
      fetchExperiments();
      document.getElementById('input-name').value = '';
      document.getElementById('input-hypothesis').value = '';
    })
    .catch(err => {
      console.error("Error:", err);
      setError(`Failed to create experiment: ${err.message}`);
      setIsLoading(false);
    });
  };

  // 2. 运行统计分析
  const handleUpdateResults = (id) => {
    const c_conv = document.getElementById(`c_conv_${id}`).value || 0;
    const c_user = document.getElementById(`c_user_${id}`).value || 0;
    const v_conv = document.getElementById(`v_conv_${id}`).value || 0;
    const v_user = document.getElementById(`v_user_${id}`).value || 0;
    
    // 基本验证
    if (parseInt(c_user) === 0 || parseInt(v_user) === 0) {
      return alert("User counts must be greater than 0");
    }

    setIsLoading(true);
    fetch(`${API_BASE}/experiments/${id}/update-results?c_conversions=${c_conv}&c_users=${c_user}&v_conversions=${v_conv}&v_users=${v_user}`, {
      method: "POST"
    })
    .then(res => {
      if (!res.ok) throw new Error(`Status: ${res.status}`);
      return res.json();
    })
    .then(data => {
      console.log("Analysis Success:", data);
      fetchExperiments();
    })
    .catch(err => {
      console.error("Error:", err);
      setError(`Failed to update results: ${err.message}`);
      setIsLoading(false);
    });
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <h1 style={{ color: '#2c3e50' }}>🔬 ExperimentOS Dashboard</h1>
      
      {/* 显示错误信息 */}
      {error && (
        <div style={{ padding: '10px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '5px', marginBottom: '20px' }}>
          {error}
        </div>
      )}
      
      {/* 显示加载状态 */}
      {isLoading && (
        <div style={{ padding: '10px', backgroundColor: '#e2f3f5', color: '#0c5460', borderRadius: '5px', marginBottom: '20px' }}>
          Loading...
        </div>
      )}
      
      {/* 注册区 */}
      <div style={{ marginBottom: '30px', background: '#fff', padding: '20px', borderRadius: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.05)' }}>
        <h3 style={{ marginTop: 0 }}>➕ Register New Experiment</h3>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input id="input-name" placeholder="Experiment Title" style={{ padding: '8px', flex: 1 }} />
          <input id="input-hypothesis" placeholder="Hypothesis" style={{ padding: '8px', flex: 2 }} />
          <button 
            onClick={handleSubmit} 
            disabled={isLoading}
            style={{ 
              padding: '8px 20px', 
              backgroundColor: isLoading ? '#bdc3c7' : '#3498db', 
              color: '#fff', 
              border: 'none', 
              borderRadius: '4px', 
              cursor: isLoading ? 'not-allowed' : 'pointer' 
            }}
          >
            Submit
          </button>
        </div>
      </div>

      {/* 实验列表 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: '20px' }}>
        {experiments.map(exp => (
          <div key={exp.id} style={{ 
            background: '#fff', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 15px rgba(0,0,0,0.08)', 
            borderLeft: exp.status && exp.status.includes('Winner') ? '8px solid #27ae60' : 
                     (exp.status && exp.status.includes('Loser') ? '8px solid #e74c3c' : '8px solid #3498db'),
            position: 'relative' 
          }}>
            {exp.is_significant && <div style={{ position: 'absolute', top: '10px', right: '10px', backgroundColor: '#27ae60', color: '#fff', padding: '5px 12px', borderRadius: '20px', fontWeight: 'bold', fontSize: '0.8em' }}>🏆 WINNER</div>}
            
            <h3>{exp.name}</h3>
            <p style={{ color: '#7f8c8d', fontSize: '0.9em' }}>{exp.hypothesis || "No hypothesis"}</p>

            {/* 输入数据 */}
            <div style={{ backgroundColor: '#f9f9f9', padding: '15px', borderRadius: '8px', marginTop: '10px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '0.8em' }}>
                <div><strong>Control (C/N)</strong><br/>
                  <input id={`c_conv_${exp.id}`} placeholder="0" style={{ width: '40px' }} /> / <input id={`c_user_${exp.id}`} placeholder="0" style={{ width: '50px' }} />
                </div>
                <div><strong>Variant (C/N)</strong><br/>
                  <input id={`v_conv_${exp.id}`} placeholder="0" style={{ width: '40px' }} /> / <input id={`v_user_${exp.id}`} placeholder="0" style={{ width: '50px' }} />
                </div>
              </div>
              <button 
                onClick={() => handleUpdateResults(exp.id)} 
                disabled={isLoading}
                style={{ 
                  width: '100%', 
                  marginTop: '10px', 
                  padding: '8px', 
                  backgroundColor: isLoading ? '#95a5a6' : '#2c3e50', 
                  color: '#fff', 
                  border: 'none', 
                  borderRadius: '4px', 
                  cursor: isLoading ? 'not-allowed' : 'pointer' 
                }}
              >
                Run Statistical Engine
              </button>
            </div>

            {/* 展示 Lift 和 Confidence Interval */}
            <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#eef2f7', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.75em', fontWeight: 'bold', color: '#555' }}>LIFT & 95% CI:</div>
              <div style={{ 
                fontSize: '1em', 
                fontWeight: 'bold', 
                color: exp.status && exp.status.includes('Winner') ? '#27ae60' : 
                       (exp.status && exp.status.includes('Loser') ? '#e74c3c' : '#2c3e50') 
              }}>
                {exp.lift || '--- (No analysis yet)'}
              </div>
            </div>

            <div style={{ marginTop: '10px', fontSize: '0.8em', color: '#7f8c8d' }}>
              <strong>P-value:</strong> {exp.p_value !== null ? exp.p_value : 'N/A'} | <strong>Status:</strong> {exp.status || 'Not analyzed'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;