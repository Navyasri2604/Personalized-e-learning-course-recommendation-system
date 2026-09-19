def generate_roadmap(career_goal):
    """
    Generates a step-by-step learning roadmap based on career goal.
    """
    goal = career_goal.lower() if career_goal else ""
    
    roadmaps = {
        'ai engineer': [
            {'step': 1, 'title': 'Python Fundamentals', 'desc': 'Learn Python syntax, data types, and control structures.'},
            {'step': 2, 'title': 'Data Structures & Algorithms', 'desc': 'Master arrays, linked lists, trees, and graphs.'},
            {'step': 3, 'title': 'Data Science Libraries', 'desc': 'Pandas, NumPy, and Matplotlib for data manipulation.'},
            {'step': 4, 'title': 'Machine Learning', 'desc': 'Supervised and unsupervised learning, Scikit-Learn.'},
            {'step': 5, 'title': 'Deep Learning', 'desc': 'Neural networks, PyTorch or TensorFlow.'},
            {'step': 6, 'title': 'NLP & Computer Vision', 'desc': 'Advanced AI applications.'},
            {'step': 7, 'title': 'MLOps', 'desc': 'Deploying and maintaining AI models in production.'}
        ],
        'data scientist': [
            {'step': 1, 'title': 'Python & SQL', 'desc': 'Learn data querying and programming basics.'},
            {'step': 2, 'title': 'Statistics & Probability', 'desc': 'Core mathematical concepts for data.'},
            {'step': 3, 'title': 'Data Visualization', 'desc': 'Tableau, PowerBI, Seaborn.'},
            {'step': 4, 'title': 'Machine Learning', 'desc': 'Predictive modeling and classification.'},
            {'step': 5, 'title': 'Big Data Tools', 'desc': 'Spark, Hadoop basics.'}
        ],
        'frontend developer': [
            {'step': 1, 'title': 'HTML & CSS', 'desc': 'Web structure and styling fundamentals.'},
            {'step': 2, 'title': 'JavaScript Basics', 'desc': 'DOM manipulation and ES6 features.'},
            {'step': 3, 'title': 'Frontend Frameworks', 'desc': 'React, Vue, or Angular.'},
            {'step': 4, 'title': 'State Management', 'desc': 'Redux or Context API.'},
            {'step': 5, 'title': 'Web Performance & Testing', 'desc': 'Optimization and Jest/Cypress.'}
        ],
        'software developer': [
            {'step': 1, 'title': 'Programming Basics (Java/C++/Python)', 'desc': 'Core language concepts.'},
            {'step': 2, 'title': 'Data Structures', 'desc': 'Algorithm optimization.'},
            {'step': 3, 'title': 'Databases', 'desc': 'SQL and NoSQL database design.'},
            {'step': 4, 'title': 'Backend Frameworks', 'desc': 'Spring Boot, Django, or Express.'},
            {'step': 5, 'title': 'System Design', 'desc': 'Architecture and scalable systems.'},
            {'step': 6, 'title': 'Version Control & CI/CD', 'desc': 'Git, GitHub Actions, Jenkins.'}
        ]
    }
    
    # Simple matching logic
    for key in roadmaps.keys():
        if key in goal:
            return roadmaps[key]
            
    # Default roadmap if no match
    return [
        {'step': 1, 'title': 'Fundamentals', 'desc': 'Learn the basic concepts of your chosen field.'},
        {'step': 2, 'title': 'Core Technologies', 'desc': 'Master the primary tools and languages.'},
        {'step': 3, 'title': 'Advanced Concepts', 'desc': 'Deep dive into specialized topics.'},
        {'step': 4, 'title': 'Projects & Portfolio', 'desc': 'Build real-world applications.'},
        {'step': 5, 'title': 'Interview Prep', 'desc': 'Prepare for industry roles.'}
    ]
