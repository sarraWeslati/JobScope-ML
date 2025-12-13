import React from 'react';
import './JobMatches.css';

const JobMatches = ({ matches }) => {
  return (
    <div className="job-matches">
      {matches.map((match, index) => (
        <div key={index} className="job-card">
          <div className="job-header">
            <div className="job-rank">#{match.rank}</div>
            <div className="job-info">
              <h3>{match.job_title}</h3>
              <p className="company">{match.company}</p>
            </div>
            <div className="match-score">
              <div className="score-circle">
                {Math.round(match.similarity_score * 100)}%
              </div>
              <span className="score-label">Match</span>
            </div>
          </div>
          
          <div className="job-details">
            <div className="detail-item">
              <span className="detail-label">📍 Location:</span>
              <span>{match.location}</span>
            </div>
            
            <div className="detail-item">
              <span className="detail-label">💰 Salary:</span>
              <span>${match.salary?.toLocaleString() || 'Not specified'}</span>
            </div>
            
            <div className="detail-item skills">
              <span className="detail-label">🔧 Required Skills:</span>
              <p>{match.required_skills}</p>
            </div>
          </div>
          
          <div className="job-actions">
            <button className="btn-secondary">Save</button>
            <button className="btn-primary">Apply Now</button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default JobMatches;
