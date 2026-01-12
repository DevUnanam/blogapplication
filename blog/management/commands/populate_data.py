from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Genre, Post, UserProfile, Follow, PostLike, Comment
from faker import Faker
import random
from django.utils import timezone
from datetime import timedelta, datetime
import pytz


class Command(BaseCommand):
    help = 'Populate the database with sample users and articles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=15,
            help='Number of users to create (default: 15)',
        )
        parser.add_argument(
            '--articles',
            type=int,
            default=50,
            help='Number of articles to create (default: 50)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        self.fake = Faker()
        self.stdout.write(self.style.SUCCESS('🌱 Starting data population...'))

        if options['clear']:
            self.clear_existing_data()

        # Ensure genres exist
        self.create_genres()

        # Create users
        users = self.create_users(options['users'])

        # Create articles
        self.create_articles(users, options['articles'])

        # Create social interactions
        self.create_social_interactions(users)

        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully populated database with {options["users"]} users and {options["articles"]} articles!')
        )

    def clear_existing_data(self):
        """Clear existing data except superusers"""
        self.stdout.write('🗑️ Clearing existing data...')

        # Clear posts and related data
        Post.objects.all().delete()
        Comment.objects.all().delete()
        PostLike.objects.all().delete()
        Follow.objects.all().delete()

        # Clear regular users (keep superusers)
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('✓ Existing data cleared')

    def create_genres(self):
        """Ensure all genres exist"""
        genres_data = [
            {'name': 'Technology', 'description': 'Latest tech trends, tutorials, and innovation'},
            {'name': 'Health & Wellness', 'description': 'Physical and mental health, fitness tips'},
            {'name': 'Travel', 'description': 'Travel guides, experiences, and adventures'},
            {'name': 'Food & Cooking', 'description': 'Recipes, restaurant reviews, culinary stories'},
            {'name': 'Lifestyle', 'description': 'Life tips, habits, and personal development'},
            {'name': 'Business & Finance', 'description': 'Money management, investing, entrepreneurship'},
            {'name': 'Entertainment', 'description': 'Movies, music, books, and pop culture'},
            {'name': 'Sports', 'description': 'Sports news, analysis, and athletic stories'},
            {'name': 'Politics', 'description': 'Political analysis and current affairs'},
            {'name': 'Education', 'description': 'Learning, teaching, and academic content'},
            {'name': 'Relationships', 'description': 'Love, dating, family, and friendships'},
            {'name': 'Personal Stories', 'description': 'Life experiences and personal narratives'},
            {'name': 'Opinion', 'description': 'Editorial content and personal viewpoints'},
            {'name': 'Science', 'description': 'Scientific discoveries and research'},
            {'name': 'Art & Culture', 'description': 'Creative arts, cultural discussions, and history'},
        ]

        for genre_data in genres_data:
            Genre.objects.get_or_create(
                name=genre_data['name'],
                defaults={'description': genre_data['description']}
            )

    def create_users(self, count):
        """Create diverse users with profiles"""
        self.stdout.write(f'👥 Creating {count} users...')

        # Predefined user data for more realistic profiles
        user_templates = [
            {'first_name': 'Sarah', 'last_name': 'Johnson', 'profession': 'Tech Writer', 'interests': ['Technology', 'Science']},
            {'first_name': 'Michael', 'last_name': 'Chen', 'profession': 'Chef', 'interests': ['Food & Cooking', 'Travel']},
            {'first_name': 'Emma', 'last_name': 'Rodriguez', 'profession': 'Fitness Coach', 'interests': ['Health & Wellness', 'Sports']},
            {'first_name': 'David', 'last_name': 'Thompson', 'profession': 'Financial Advisor', 'interests': ['Business & Finance', 'Lifestyle']},
            {'first_name': 'Jessica', 'last_name': 'Wilson', 'profession': 'Travel Blogger', 'interests': ['Travel', 'Art & Culture']},
            {'first_name': 'James', 'last_name': 'Brown', 'profession': 'Sports Journalist', 'interests': ['Sports', 'Entertainment']},
            {'first_name': 'Ashley', 'last_name': 'Davis', 'profession': 'Relationship Counselor', 'interests': ['Relationships', 'Personal Stories']},
            {'first_name': 'Ryan', 'last_name': 'Martinez', 'profession': 'Political Analyst', 'interests': ['Politics', 'Opinion']},
            {'first_name': 'Amanda', 'last_name': 'Garcia', 'profession': 'Teacher', 'interests': ['Education', 'Personal Stories']},
            {'first_name': 'Christopher', 'last_name': 'Lee', 'profession': 'Food Critic', 'interests': ['Food & Cooking', 'Lifestyle']},
            {'first_name': 'Jennifer', 'last_name': 'Taylor', 'profession': 'Wellness Coach', 'interests': ['Health & Wellness', 'Lifestyle']},
            {'first_name': 'Daniel', 'last_name': 'Anderson', 'profession': 'Movie Critic', 'interests': ['Entertainment', 'Art & Culture']},
            {'first_name': 'Nicole', 'last_name': 'White', 'profession': 'Entrepreneur', 'interests': ['Business & Finance', 'Technology']},
            {'first_name': 'Kevin', 'last_name': 'Jackson', 'profession': 'Science Writer', 'interests': ['Science', 'Education']},
            {'first_name': 'Megan', 'last_name': 'Harris', 'profession': 'Life Coach', 'interests': ['Lifestyle', 'Personal Stories']},
        ]

        created_users = []

        for i in range(count):
            if i < len(user_templates):
                template = user_templates[i]
                first_name = template['first_name']
                last_name = template['last_name']
                profession = template['profession']
            else:
                first_name = self.fake.first_name()
                last_name = self.fake.last_name()
                profession = self.fake.job()

            username = f"{first_name.lower()}_{last_name.lower()}"
            email = f"{username}@example.com"

            # Create user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': 'pbkdf2_sha256$600000$test$test',  # Password: 'test'
                    'is_active': True,
                    'date_joined': timezone.make_aware(self.fake.date_time_between(start_date='-2y', end_date='now')),
                }
            )

            if created:
                # Create user profile
                bio_templates = [
                    f"Passionate {profession.lower()} sharing insights and experiences.",
                    f"Welcome to my corner of the internet! I'm a {profession.lower()} who loves to write.",
                    f"{profession} by day, writer by passion. Sharing stories that matter.",
                    f"Experienced {profession.lower()} with a love for storytelling.",
                    f"Join me as I explore life as a {profession.lower()} and share my journey.",
                ]

                profile, _ = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'bio': random.choice(bio_templates),
                        'location': self.fake.city(),
                        'website': f"https://{username}.com" if random.choice([True, False]) else "",
                        'dark_mode': random.choice([True, False]),
                    }
                )

                created_users.append(user)
                self.stdout.write(f'  ✓ Created user: {user.username}')
            else:
                created_users.append(user)
                self.stdout.write(f'  - User already exists: {user.username}')

        return created_users

    def create_articles(self, users, count):
        """Create diverse articles across all genres"""
        self.stdout.write(f'📝 Creating {count} articles...')

        genres = list(Genre.objects.all())
        if not genres:
            self.stdout.write(self.style.ERROR('No genres found! Please run setup_blog command first.'))
            return

        # Article templates for different genres
        article_templates = {
            'Technology': [
                ('The Future of Artificial Intelligence', 'Exploring how AI is revolutionizing industries and changing the way we work and live.'),
                ('Cybersecurity in 2026', 'Essential security practices every internet user should know to protect their digital life.'),
                ('The Rise of Quantum Computing', 'Understanding quantum technology and its potential impact on computing.'),
                ('Sustainable Tech Solutions', 'How technology companies are going green and reducing their environmental footprint.'),
                ('5G and Beyond: The Next Generation', 'Examining the latest developments in telecommunications technology.'),
            ],
            'Health & Wellness': [
                ('Mental Health in the Digital Age', 'Strategies for maintaining mental wellness while staying connected.'),
                ('The Science of Sleep', 'Understanding sleep cycles and how to improve your rest quality.'),
                ('Nutrition Myths Debunked', 'Separating fact from fiction in popular diet trends.'),
                ('Exercise for Busy Professionals', 'Simple workout routines that fit into a hectic schedule.'),
                ('Mindfulness and Meditation', 'Practical approaches to reducing stress and finding inner peace.'),
            ],
            'Travel': [
                ('Hidden Gems of Southeast Asia', 'Discovering off-the-beaten-path destinations for the adventurous traveler.'),
                ('Solo Travel Safety Tips', 'Essential advice for traveling alone with confidence.'),
                ('Budget Travel Hacks', 'How to see the world without breaking the bank.'),
                ('Cultural Etiquette Around the World', 'Avoiding common cultural mistakes when traveling abroad.'),
                ('Sustainable Tourism Practices', 'How to travel responsibly and protect the places we visit.'),
            ],
            'Food & Cooking': [
                ('Farm-to-Table Movement', 'Exploring the benefits of locally sourced ingredients.'),
                ('International Street Food Guide', 'A culinary journey through global street food cultures.'),
                ('Plant-Based Cooking for Beginners', 'Simple and delicious recipes for a healthier lifestyle.'),
                ('The Art of Fermentation', 'Traditional fermentation techniques and their health benefits.'),
                ('Seasonal Cooking Tips', 'Making the most of fresh, seasonal ingredients.'),
            ],
            'Business & Finance': [
                ('Personal Finance in Your 20s', 'Building a strong financial foundation early in life.'),
                ('The Gig Economy Revolution', 'Understanding the changing landscape of work and employment.'),
                ('Investing for Beginners', 'Simple strategies for growing your wealth over time.'),
                ('Remote Work Best Practices', 'Maximizing productivity while working from home.'),
                ('Cryptocurrency Explained', 'A beginner\'s guide to digital currencies and blockchain technology.'),
            ],
        }

        # Generate additional generic templates for other genres
        generic_templates = [
            ('Lessons Learned', 'Reflecting on important life experiences and the wisdom they provide.'),
            ('Breaking Down Barriers', 'Overcoming challenges and obstacles in pursuit of our goals.'),
            ('The Power of Community', 'How building connections can transform our lives and society.'),
            ('Finding Your Voice', 'Discovering your unique perspective and sharing it with the world.'),
            ('Innovation and Creativity', 'Exploring new ideas and thinking outside the box.'),
        ]

        created_articles = 0

        for i in range(count):
            # Select random author and genre
            author = random.choice(users)
            genre = random.choice(genres)

            # Get article template
            if genre.name in article_templates:
                template = random.choice(article_templates[genre.name])
            else:
                template = random.choice(generic_templates)

            title_base, content_base = template

            # Add variation to avoid duplicates
            title = f"{title_base}: A {random.choice(['Personal', 'Professional', 'Deep', 'Comprehensive', 'Practical'])} Perspective"

            # Generate comprehensive content
            content_parts = [
                content_base,
                "\n\n" + self.fake.text(max_nb_chars=800),
                "\n\n" + self.fake.text(max_nb_chars=600),
                "\n\n" + "What are your thoughts on this topic? I'd love to hear your experiences in the comments below!",
            ]
            content = "".join(content_parts)

            # Create the post with varied creation dates
            creation_date = timezone.make_aware(self.fake.date_time_between(
                start_date='-6m',
                end_date='now'
            ))

            try:
                post = Post.objects.create(
                    title=title,
                    content=content,
                    author=author,
                    genre=genre,
                    created_at=creation_date,
                    updated_at=creation_date + timedelta(hours=random.randint(0, 48)),
                    is_published=True,
                )

                created_articles += 1
                if created_articles <= 10:  # Show first 10 for brevity
                    self.stdout.write(f'  ✓ Created: "{post.title}" by {author.username}')
                elif created_articles == 11:
                    self.stdout.write('  ... (continuing to create more articles)')

            except Exception as e:
                self.stdout.write(f'  ❌ Failed to create article: {e}')

        self.stdout.write(f'✅ Created {created_articles} articles successfully!')

    def create_social_interactions(self, users):
        """Create follows, likes, and comments for realistic social interaction"""
        self.stdout.write('🤝 Creating social interactions...')

        posts = list(Post.objects.all())
        if not posts:
            return

        # Create follow relationships
        follow_count = 0
        for user in users[:12]:  # Not all users need to follow everyone
            # Each user follows 3-8 random other users
            follow_targets = random.sample([u for u in users if u != user], k=random.randint(3, 8))
            for target in follow_targets:
                follow, created = Follow.objects.get_or_create(
                    follower=user,
                    following=target,
                )
                if created:
                    follow_count += 1

        # Create post likes
        like_count = 0
        for post in posts:
            # Each post gets likes from 0-15 users
            likers = random.sample(users, k=random.randint(0, min(15, len(users))))
            for liker in likers:
                if liker != post.author:  # Users don't like their own posts
                    like, created = PostLike.objects.get_or_create(
                        user=liker,
                        post=post,
                    )
                    if created:
                        like_count += 1

        # Create comments
        comment_count = 0
        comment_templates = [
            "Great article! Thanks for sharing your insights.",
            "This really resonates with me. I had a similar experience.",
            "Interesting perspective! I never thought about it that way.",
            "Thanks for the detailed explanation. Very helpful!",
            "I disagree with some points, but appreciate the discussion.",
            "Could you elaborate more on this topic?",
            "This is exactly what I needed to read today.",
            "Fantastic writing! Looking forward to more posts.",
            "I learned something new. Thank you for this!",
            "Well researched and thoughtfully written.",
        ]

        for post in random.sample(posts, k=min(30, len(posts))):  # Add comments to 30 random posts
            # Each selected post gets 1-5 comments
            num_comments = random.randint(1, 5)
            commenters = random.sample([u for u in users if u != post.author], k=min(num_comments, len(users)-1))

            for commenter in commenters:
                comment = Comment.objects.create(
                    post=post,
                    author=commenter,
                    content=random.choice(comment_templates),
                    created_at=post.created_at + timedelta(
                        hours=random.randint(1, 168)  # Comments within a week of post
                    )
                )
                comment_count += 1

        self.stdout.write(f'  ✓ Created {follow_count} follow relationships')
        self.stdout.write(f'  ✓ Created {like_count} post likes')
        self.stdout.write(f'  ✓ Created {comment_count} comments')