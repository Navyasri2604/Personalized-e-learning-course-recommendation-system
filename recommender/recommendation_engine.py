import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Course

def get_recommendations(user_profile):
    """
    Returns top 10 recommended courses based on user profile.
    Uses TF-IDF Vectorizer and Cosine Similarity.
    """
    courses = Course.objects.all()
    if not courses.exists():
        return []

    # Create a DataFrame for courses
    course_data = []
    for c in courses:
        # Combine relevant text fields for vectorization
        combined_text = f"{c.category} {c.difficulty} {c.skills} {c.description} {c.course_name}"
        course_data.append({
            'id': c.id,
            'combined_text': combined_text.lower()
        })
    
    df = pd.DataFrame(course_data)

    # Create user profile text
    user_interests = user_profile.interests or ""
    user_skills = user_profile.skills or ""
    user_goal = user_profile.career_goal or ""
    
    user_text = f"{user_interests} {user_skills} {user_goal}".lower()
    
    # If user has no preferences, return highest rated
    if not user_text.strip():
        return Course.objects.order_by('-rating')[:10]

    # Combine user text and course texts
    all_texts = [user_text] + df['combined_text'].tolist()

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Calculate Cosine Similarity between user (index 0) and courses (index 1 onwards)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Get top 10 indices
    top_indices = cosine_sim.argsort()[-10:][::-1]
    
    # Get course IDs
    recommended_course_ids = df.iloc[top_indices]['id'].tolist()
    
    # Fetch courses from DB maintaining order
    recommended_courses = []
    for cid in recommended_course_ids:
        recommended_courses.append(Course.objects.get(id=cid))
        
    return recommended_courses
