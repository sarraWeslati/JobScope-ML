import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import joblib
from flask import current_app

class CVMatchingService:
    """Service pour matcher les CVs avec les offres d'emploi en utilisant LDA topic modeling"""
    
    def __init__(self):
        self.df_jobs = None
        self.lda_model = None
        self.count_vectorizer = None
        self.job_topic_distributions = None
        self.load_and_prepare()
    
    def load_and_prepare(self):
        """Charger le modèle LDA et les données pré-calculées"""
        try:
            # Chemins des fichiers du modèle LDA
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            model_dir = os.path.join(backend_dir, 'final_model')
            
            # Charger le modèle LDA
            lda_path = os.path.join(model_dir, 'lda_model.joblib')
            self.lda_model = joblib.load(lda_path)
            print(f"[OK] Modele LDA charge avec {self.lda_model.n_components} topics")
            
            # Charger le CountVectorizer (CRITIQUE - nécessaire pour transformer les nouveaux CVs)
            vectorizer_path = os.path.join(model_dir, 'count_vectorizer.joblib')
            self.count_vectorizer = joblib.load(vectorizer_path)
            print(f"[OK] CountVectorizer charge: {len(self.count_vectorizer.vocabulary_)} mots")
            
            # Charger les distributions de topics pré-calculées pour les jobs
            job_topics_path = os.path.join(model_dir, 'job_topic_distributions.joblib')
            self.job_topic_distributions = joblib.load(job_topics_path)
            print(f"[OK] Distributions de topics chargees: {self.job_topic_distributions.shape[0]} jobs")
            
            # Charger le DataFrame des jobs
            jobs_pkl = os.path.join(model_dir, 'jobs_dataframe.pkl')
            self.df_jobs = pd.read_pickle(jobs_pkl)
            print(f"[OK] Jobs charges: {len(self.df_jobs)} offres")
            
        except Exception as e:
            print(f"[ERROR] Erreur lors du chargement du modele: {e}")
            raise
    
    def match_cv(self, cv_text, top_n=5):
        """
        Matcher un CV avec les meilleures offres en utilisant LDA topic modeling
        
        Args:
            cv_text: Texte extrait du CV
            top_n: Nombre de top résultats (défaut: 5)
        
        Returns:
            Liste des top N offres avec scores de similarité
        """
        try:
            if not cv_text or cv_text.strip() == '':
                return {
                    'success': False,
                    'error': 'CV text is empty',
                    'matches': []
                }
            
            # 1. Vectoriser le CV avec CountVectorizer
            cv_count = self.count_vectorizer.transform([cv_text])
            
            # 2. Transformer en distribution de topics avec LDA
            cv_topic_distribution = self.lda_model.transform(cv_count)
            
            # 3. Calculer les similarités cosine avec tous les jobs
            similarities = cosine_similarity(cv_topic_distribution, self.job_topic_distributions).flatten()
            
            # 4. Obtenir les indices des top N
            top_indices = np.argsort(similarities)[::-1][:top_n]
            
            # 5. Construire les résultats
            matches = []
            for rank, idx in enumerate(top_indices, 1):
                job = self.df_jobs.iloc[idx]
                match = {
                    'rank': rank,
                    'job_title': str(job['job_title']) if 'job_title' in job.index else 'N/A',
                    'company': str(job['company_name']) if 'company_name' in job.index else 'N/A',
                    'location': str(job['company_location']) if 'company_location' in job.index else 'N/A',
                    'salary': float(job['salary_usd']) if 'salary_usd' in job.index and pd.notna(job['salary_usd']) else None,
                    'experience_level': str(job['experience_level']) if 'experience_level' in job.index else 'N/A',
                    'required_skills': str(job['required_skills'])[:200] if 'required_skills' in job.index else 'N/A',
                    'similarity_score': float(similarities[idx])
                }
                matches.append(match)
            
            return {
                'success': True,
                'matches': matches,
                'cv_length': len(cv_text),
                'total_jobs_searched': len(self.df_jobs),
                'model_type': 'LDA',
                'n_topics': self.lda_model.n_components
            }
            
        except Exception as e:
            print(f"[ERROR] Erreur lors du matching: {e}")
            return {
                'success': False,
                'error': str(e),
                'matches': []
            }
    
    def get_job_stats(self):
        """Retourner les statistiques des jobs"""
        try:
            stats = {
                'total_jobs': len(self.df_jobs),
                'avg_salary': float(self.df_jobs['salary_usd'].mean()) if 'salary_usd' in self.df_jobs.columns else 0,
                'locations': self.df_jobs['company_location'].nunique() if 'company_location' in self.df_jobs.columns else 0,
                'experience_levels': self.df_jobs['experience_level'].unique().tolist() if 'experience_level' in self.df_jobs.columns else [],
            }
            return stats
        except Exception as e:
            print(f"[ERROR] Erreur lors des stats: {e}")
            return {}


# Instance globale
cv_matching_service = None

def get_cv_matching_service():
    """Récupérer ou créer l'instance du service"""
    global cv_matching_service
    if cv_matching_service is None:
        cv_matching_service = CVMatchingService()
    return cv_matching_service
