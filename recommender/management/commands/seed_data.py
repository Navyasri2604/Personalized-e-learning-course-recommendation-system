from django.core.management.base import BaseCommand
from recommender.models import Course
import random

class Command(BaseCommand):
    help = 'Seeds the database with 500+ realistic courses'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting existing courses...')
        Course.objects.all().delete()
        
        universities = ['Google', 'Microsoft', 'IBM', 'AWS', 'Coursera', 'Udemy', 'Stanford', 'Harvard', 'MIT', 'edX']
        difficulties = ['Beginner', 'Intermediate', 'Advanced']
        
        categories = {
            'Programming': ['Python', 'Java', 'C++', 'JavaScript', 'Go', 'Ruby', 'Rust', 'Swift'],
            'AI and Machine Learning': ['Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision', 'Generative AI', 'Reinforcement Learning'],
            'Data Science': ['Python for Data Science', 'SQL', 'Power BI', 'Tableau', 'Statistics', 'Data Analytics', 'Big Data'],
            'Cloud': ['AWS', 'Azure', 'Google Cloud', 'Cloud Architecture', 'DevOps on Cloud'],
            'Cyber Security': ['Ethical Hacking', 'Network Security', 'SOC Analyst', 'Cryptography', 'Cyber Defense'],
            'Testing': ['Manual Testing', 'Selenium', 'API Testing', 'Automation Testing', 'QA Engineering'],
            'Business': ['Business Analytics', 'Product Management', 'Digital Marketing', 'Agile Methodology', 'Scrum']
        }

        courses_to_create = []
        count = 0
        
        # Generate courses for each category and sub-topic
        for cat, topics in categories.items():
            for topic in topics:
                # Generate about 10-15 courses per topic to reach ~500 total
                num_courses = random.randint(10, 15)
                for i in range(num_courses):
                    difficulty = random.choice(difficulties)
                    uni = random.choice(universities)
                    rating = round(random.uniform(3.5, 5.0), 1)
                    duration = f"{random.randint(2, 40)} weeks"
                    
                    course_name = f"{difficulty} {topic} Masterclass by {uni}"
                    if random.random() > 0.5:
                        course_name = f"Complete {topic} Bootcamp ({difficulty})"
                        
                    description = f"This course covers comprehensive aspects of {topic}. Designed for {difficulty} learners, you will learn the fundamental and advanced concepts required to master {cat}."
                    
                    skills = f"{topic}, {cat}, Problem Solving, Real-world Projects"
                    if cat == 'Programming':
                        skills += ", Coding, Algorithms"
                    elif cat == 'AI and Machine Learning':
                        skills += ", Models, Neural Networks"
                        
                    url = f"https://www.example.com/course/{topic.replace(' ', '-').lower()}-{i}"
                    
                    courses_to_create.append(
                        Course(
                            course_name=course_name,
                            university=uni,
                            category=cat,
                            difficulty=difficulty,
                            rating=rating,
                            duration=duration,
                            description=description,
                            skills=skills,
                            course_url=url
                        )
                    )
                    count += 1

        self.stdout.write(f'Creating {count} courses...')
        Course.objects.bulk_create(courses_to_create)
        self.stdout.write(self.style.SUCCESS('Successfully seeded database with realistic courses!'))
