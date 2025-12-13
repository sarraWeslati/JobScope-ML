"""
Script to train and save the LDA-based job matching model
This replaces the old TF-IDF based approach with LDA topic modeling
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity

def ensure_text(df, candidates=None, target='Text'):
    """Ensure DataFrame has a unified 'Text' column"""
    if target in df.columns:
        df[target] = df[target].astype(str).str.strip().replace('', 'missing_text')
        return df

    use_cols = [c for c in (candidates or []) if c in df.columns]
    if not use_cols:
        obj_cols = [c for c in df.columns if df[c].dtype == 'object']
        use_cols = obj_cols
    if not use_cols:
        raise ValueError("No suitable text columns available to construct 'Text'.")

    df[target] = (
        df[use_cols]
          .astype(str)
          .apply(lambda row: ' '.join([v for v in row if v and v.lower() != 'nan']).strip(), axis=1)
          .replace('', 'missing_text')
    )
    return df


def main():
    print("=" * 80)
    print("TRAINING LDA-BASED JOB MATCHING MODEL")
    print("=" * 80)
    
    # Paths
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    model_dir = os.path.join(os.path.dirname(__file__), 'final_model')
    os.makedirs(model_dir, exist_ok=True)
    
    # Load datasets
    print("\n[1/5] Loading datasets...")
    jobs_path = os.path.join(data_dir, 'ai_job_dataset.csv')
    cv_path = os.path.join(data_dir, 'dataset_cvs_cleaned.csv')
    
    if not os.path.exists(jobs_path):
        raise FileNotFoundError(f"Jobs dataset not found at: {jobs_path}")
    
    df_jobs = pd.read_csv(jobs_path)
    
    # Try to load CV dataset if it exists (for training purposes)
    if os.path.exists(cv_path):
        df_cv = pd.read_csv(cv_path)
        print(f"✅ Loaded {len(df_cv)} CVs and {len(df_jobs)} jobs")
    else:
        print(f"⚠️ CV dataset not found, will train on jobs only")
        df_cv = pd.DataFrame()
    
    # Prepare text columns
    print("\n[2/5] Preparing text data...")
    job_candidates = ['job_text', 'job_title', 'required_skills', 'education_required', 
                     'industry', 'company_name', 'job_description', 'description']
    df_jobs = ensure_text(df_jobs, candidates=job_candidates, target='Text')
    
    if len(df_cv) > 0:
        cv_candidates = ['cv_text', 'Skills', 'Education', 'Certifications', 
                        'Job Role', 'Summary', 'Experience', 'Experience (Years)']
        df_cv = ensure_text(df_cv, candidates=cv_candidates, target='Text')
    
    print(f"✅ Text column created for {len(df_jobs)} jobs")
    
    # Vectorize with CountVectorizer (needed for LDA)
    print("\n[3/5] Vectorizing text with CountVectorizer...")
    count_vec = CountVectorizer(
        max_features=5000, 
        stop_words='english',
        max_df=0.95,
        min_df=2
    )
    
    if len(df_cv) > 0:
        # Fit on both CVs and jobs for better vocabulary
        all_texts = pd.concat([df_cv['Text'], df_jobs['Text']], ignore_index=True)
        count_vec.fit(all_texts)
        job_count = count_vec.transform(df_jobs['Text'])
    else:
        # Fit on jobs only
        job_count = count_vec.fit_transform(df_jobs['Text'])
    
    print(f"✅ Vectorization complete: {job_count.shape}")
    
    # Train LDA model
    print("\n[4/5] Training LDA model with 10 topics...")
    final_lda = LatentDirichletAllocation(
        n_components=10,              # best from hyperparameter tuning
        max_iter=50,
        learning_method='online',
        learning_offset=50,
        random_state=42,
        batch_size=128,
        verbose=0
    )
    
    # Fit and transform jobs
    final_job_topics = final_lda.fit_transform(job_count)
    print(f"✅ LDA model trained successfully")
    print(f"   - Topics: {final_lda.n_components}")
    print(f"   - Job topic distribution shape: {final_job_topics.shape}")
    
    # Save all artifacts
    print("\n[5/5] Saving model artifacts...")
    
    # 1. LDA model
    joblib.dump(final_lda, os.path.join(model_dir, 'lda_model.joblib'))
    print("   ✓ lda_model.joblib")
    
    # 2. CountVectorizer (CRITICAL - needed to process new CVs)
    joblib.dump(count_vec, os.path.join(model_dir, 'count_vectorizer.joblib'))
    print("   ✓ count_vectorizer.joblib")
    
    # 3. Pre-computed job topic distributions (for fast matching)
    joblib.dump(final_job_topics, os.path.join(model_dir, 'job_topic_distributions.joblib'))
    print("   ✓ job_topic_distributions.joblib")
    
    # 4. Jobs DataFrame (with all metadata for display)
    df_jobs.to_pickle(os.path.join(model_dir, 'jobs_dataframe.pkl'))
    print("   ✓ jobs_dataframe.pkl")
    
    # Also save as CSV for easy inspection
    df_jobs.to_csv(os.path.join(model_dir, 'jobs_dataframe.csv'), index=False)
    print("   ✓ jobs_dataframe.csv")
    
    print("\n" + "=" * 80)
    print("✅ MODEL TRAINING COMPLETE!")
    print("=" * 80)
    print(f"\nAll artifacts saved in: {model_dir}")
    print("\nModel is ready to use in the API!")
    
    # Quick validation
    print("\n[Validation] Testing model with sample CV text...")
    sample_cv = "Python developer with 5 years experience in machine learning and deep learning"
    cv_count = count_vec.transform([sample_cv])
    cv_topics = final_lda.transform(cv_count)
    similarities = cosine_similarity(cv_topics, final_job_topics).flatten()
    top_5_idx = np.argsort(similarities)[-5:][::-1]
    
    print(f"\nTop 5 job matches for sample CV:")
    for i, idx in enumerate(top_5_idx, 1):
        job_title = df_jobs.iloc[idx].get('job_title', 'N/A')
        company = df_jobs.iloc[idx].get('company_name', 'N/A')
        score = similarities[idx]
        print(f"  {i}. {job_title} at {company} - Score: {score:.4f}")
    
    print("\n✅ Validation successful!")


if __name__ == '__main__':
    main()
