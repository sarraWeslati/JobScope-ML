import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { cvService } from '../services/api';
import CVUpload from '../components/CVUpload';
import JobMatches from '../components/JobMatches';
import './Dashboard.css';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [matches, setMatches] = useState([]);
  const [history, setHistory] = useState([]);
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Only load history if user is authenticated
    if (isAuthenticated()) {
      loadHistory();
    }
  }, []);

  const loadHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.warn('No token found, skipping history load');
        return;
      }
      const data = await cvService.getHistory();
      setHistory(data.history || []);
    } catch (error) {
      console.error('Error loading history:', error);
      // Only show error if it's not a 422 on initial load
      if (error.response?.status !== 422) {
        console.error('Failed to load history');
      }
    }
  };

  const handleUploadSuccess = (data) => {
    setMatches(data.top_5_matches || data.matches || []);
    setActiveTab('matches');
    loadHistory();
  };

  const handleDeleteCV = async (cvId) => {
    if (window.confirm('Are you sure you want to delete this CV?')) {
      try {
        await cvService.deleteCV(cvId);
        loadHistory(); // Reload history after deletion
      } catch (error) {
        console.error('Error deleting CV:', error);
        alert('Failed to delete CV');
      }
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <div className="nav-brand">
          <h1>Job Scope</h1>
        </div>
        <div className="nav-user">
          <span>Welcome, {user?.full_name || user?.email}</span>
          <button onClick={handleLogout} className="btn-secondary">Logout</button>
        </div>
      </nav>

      <div className="dashboard-content">
        <aside className="sidebar">
          <ul className="sidebar-menu">
            <li 
              className={activeTab === 'upload' ? 'active' : ''}
              onClick={() => setActiveTab('upload')}
            >
              📤 Upload CV
            </li>
            <li 
              className={activeTab === 'matches' ? 'active' : ''}
              onClick={() => setActiveTab('matches')}
            >
              🎯 Job Matches
            </li>
            <li 
              className={activeTab === 'history' ? 'active' : ''}
              onClick={() => setActiveTab('history')}
            >
              📋 My Uploaded CV
            </li>
          </ul>
        </aside>

        <main className="main-content">
          {activeTab === 'upload' && (
            <div className="tab-content">
              <h2>Upload Your CV</h2>
              <p>Upload your CV to get matched with the top 5 jobs that fit your profile</p>
              <CVUpload onUploadSuccess={handleUploadSuccess} />
            </div>
          )}

          {activeTab === 'matches' && (
            <div className="tab-content">
              <h2>Your Job Matches</h2>
              {matches.length > 0 ? (
                <JobMatches matches={matches} />
              ) : (
                <p className="empty-state">No matches yet. Upload your CV to get started!</p>
              )}
            </div>
          )}

          {activeTab === 'history' && (
            <div className="tab-content">
              <h2>My Uploaded CV</h2>
              {history.length > 0 ? (
                <div className="history-list">
                  {history.map((item) => (
                    <div key={item.id} className="history-item">
                      <div className="history-header">
                        <h3>{item.filename}</h3>
                        <span className="date">{new Date(item.uploaded_at).toLocaleDateString()}</span>
                      </div>
                      <p className="skills">{item.skills}</p>
                      <div className="history-actions">
                        <button 
                          className="btn-link"
                          onClick={() => {
                            setMatches(item.matches || []);
                            setActiveTab('matches');
                          }}
                        >
                          View {item.matches?.length || 0} matches
                        </button>
                        <button 
                          className="btn-delete"
                          onClick={() => handleDeleteCV(item.id)}
                        >
                          🗑️ Delete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="empty-state">No upload history yet.</p>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
