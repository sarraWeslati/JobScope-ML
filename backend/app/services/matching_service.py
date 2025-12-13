import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
from flask import current_app

class JobMatchingService:
    """Service de matching de jobs utilisant LDA topic modeling"""
    
    def __init__(self):
        self.lda_model = None
        self.count_vectorizer = None
        self.job_topic_distributions = None
        self.jobs_df = None
        self.load_model()
    
    def load_model(self):
        """Charger le modèle LDA pré-entrainé"""
        try:
            # Déterminer le chemin du modèle
            if current_app:
                backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            else:
                backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            model_dir = os.path.join(backend_dir, 'final_model')
            
            # Charger tous les composants
            self.lda_model = joblib.load(os.path.join(model_dir, 'lda_model.joblib'))
            self.count_vectorizer = joblib.load(os.path.join(model_dir, 'count_vectorizer.joblib'))
            self.job_topic_distributions = joblib.load(os.path.join(model_dir, 'job_topic_distributions.joblib'))
            self.jobs_df = pd.read_pickle(os.path.join(model_dir, 'jobs_dataframe.pkl'))
            
            print(f"[OK] Modele LDA charge: {self.lda_model.n_components} topics, {len(self.jobs_df)} jobs")
            
        except Exception as e:
            print(f"[ERROR] Erreur lors du chargement du modele: {e}")
            # Fallback: créer un dataset minimal
            self.jobs_df = pd.DataFrame({
                'job_title': ['Data Scientist', 'ML Engineer', 'AI Researcher'],
                'company_name': ['Company A', 'Company B', 'Company C'],
                'company_location': ['New York', 'San Francisco', 'Boston'],
                'salary_usd': [120000, 140000, 130000],
                'required_skills': ['Python, ML, Statistics', 'Python, TensorFlow, Deep Learning', 'Python, NLP, Research']
            })
    
    def find_top_matches(self, cv_text, top_n=5):
        """
        Trouver les top N jobs correspondant au CV en utilisant LDA
        
        Args:
            cv_text: Texte du CV
            top_n: Nombre de résultats
        
        Returns:
            Dictionnaire avec les matches et métadonnées
        """
        try:
            if not cv_text or cv_text.strip() == '':
                return {
                    'success': False,
                    'error': 'CV text is empty',
                    'matches': []
                }
            
            # 1. Vectoriser avec CountVectorizer
            cv_count = self.count_vectorizer.transform([cv_text])
            
            # 2. Obtenir la distribution de topics
            cv_topics = self.lda_model.transform(cv_count)
            
            # 3. Calculer similarités avec tous les jobs
            similarity_scores = cosine_similarity(cv_topics, self.job_topic_distributions)[0]
            
            # 4. Top N indices
            top_indices = np.argsort(similarity_scores)[-top_n:][::-1]
            
            # 5. Construire les résultats
            matches = []
            for rank, idx in enumerate(top_indices, 1):
                job = self.jobs_df.iloc[idx]
                match = {
                    'rank': rank,
                    'job_title': job.get('job_title', 'N/A'),
                    'company': job.get('company_name', job.get('company_location', 'N/A')),
                    'location': job.get('company_location', 'N/A'),
                    'salary': float(job.get('salary_usd', 0)) if pd.notna(job.get('salary_usd', 0)) else None,
                    'required_skills': str(job.get('required_skills', 'N/A'))[:200],
                    'similarity_score': float(similarity_scores[idx])
                }
                matches.append(match)
            
            return {
                'success': True,
                'matches': matches,
                'model_type': 'LDA',
                'n_topics': self.lda_model.n_components
            }
            
        except Exception as e:
            print(f"[ERROR] Erreur lors du matching: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'matches': []
            }

# Global instance
matching_service = None

def get_matching_service():
    """Get or create the matching service instance"""
    global matching_service
    if matching_service is None:
        matching_service = JobMatchingService()
    return matching_service
