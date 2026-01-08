from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Genre, UserProfile


class Command(BaseCommand):
    help = 'Set up the blog with initial genres and sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser account',
        )
        parser.add_argument(
            '--create-sample-data',
            action='store_true',
            help='Create sample posts and users',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧽 Setting up Tori\'s Blog...'))

        # Create genres
        self.create_genres()
        
        # Create superuser if requested
        if options['create_superuser']:
            self.create_superuser()
        
        # Create sample data if requested
        if options['create_sample_data']:
            self.create_sample_data()
            
        self.stdout.write(
            self.style.SUCCESS('✅ Blog setup complete! Ready to share amazing stories!')
        )

    def create_genres(self):
        """Create the 15 required genres"""
        genres_data = [
            {'name': 'Sports', 'description': 'Sports news, analysis, and personal stories'},
            {'name': 'Comedy', 'description': 'Funny stories, jokes, and humorous content'},
            {'name': 'Technology', 'description': 'Tech news, tutorials, and innovation'},
            {'name': 'Politics', 'description': 'Political analysis and current affairs'},
            {'name': 'Lifestyle', 'description': 'Life tips, habits, and personal development'},
            {'name': 'Relationships', 'description': 'Love, dating, family, and friendships'},
            {'name': 'Finance', 'description': 'Money management, investing, and economics'},
            {'name': 'Education', 'description': 'Learning, teaching, and academic content'},
            {'name': 'Health', 'description': 'Wellness, fitness, and medical information'},
            {'name': 'Travel', 'description': 'Travel guides, experiences, and adventures'},
            {'name': 'Entertainment', 'description': 'Movies, music, books, and pop culture'},
            {'name': 'Food', 'description': 'Recipes, restaurant reviews, and culinary stories'},
            {'name': 'Religion', 'description': 'Faith, spirituality, and religious discussions'},
            {'name': 'Personal Stories', 'description': 'Life experiences and personal narratives'},
            {'name': 'Opinion', 'description': 'Editorial content and personal viewpoints'},
        ]
        
        created_count = 0
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'],
                defaults={'description': genre_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✓ Created genre: {genre.name}')
            else:
                self.stdout.write(f'  - Genre already exists: {genre.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'📁 Genres setup complete! Created {created_count} new genres.')
        )

    def create_superuser(self):
        """Create a superuser account"""
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('  - Superuser already exists')
            return
            
        username = input('Enter superuser username: ') or 'admin'
        email = input('Enter superuser email: ') or 'admin@toriblog.com'
        password = input('Enter superuser password: ') or 'admin123'
        
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS(f'👑 Superuser "{username}" created successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to create superuser: {e}')
            )

    def create_sample_data(self):
        """Create sample users and posts"""
        from blog.models import Post
        import random
        
        # Create sample users
        sample_users_data = [
            {'username': 'alice_writer', 'first_name': 'Alice', 'last_name': 'Johnson', 'email': 'alice@example.com'},
            {'username': 'bob_blogger', 'first_name': 'Bob', 'last_name': 'Smith', 'email': 'bob@example.com'},
            {'username': 'carol_creator', 'first_name': 'Carol', 'last_name': 'Davis', 'email': 'carol@example.com'},
        ]
        
        created_users = []
        for user_data in sample_users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                    'password': 'pbkdf2_sha256$600000$test$test'  # Default password: 'test'
                }
            )
            if created:
                created_users.append(user)
                self.stdout.write(f'  ✓ Created user: {user.username}')
            else:
                self.stdout.write(f'  - User already exists: {user.username}')
        
        # Create sample posts
        if created_users:
            sample_posts_data = [
                {
                    'title': 'Welcome to Tori\'s Blog!',
                    'content': 'This is our first post on this amazing new blogging platform. We\'re excited to share stories, connect with readers, and build a thriving community of writers and storytellers.',
                    'genre': 'Personal Stories'
                },
                {
                    'title': 'The Future of Technology',
                    'content': 'Exploring the latest trends in technology and how they\'re shaping our world. From AI to blockchain, let\'s dive into what\'s coming next.',
                    'genre': 'Technology'
                },
                {
                    'title': 'Healthy Living Tips',
                    'content': 'Simple tips and tricks for maintaining a healthy lifestyle. Learn about nutrition, exercise, and mental wellness.',
                    'genre': 'Health'
                },
                {
                    'title': 'Travel Adventures Await',
                    'content': 'Discover amazing destinations and travel tips from around the world. Let\'s explore together!',
                    'genre': 'Travel'
                },
                {
                    'title': 'Cooking Made Simple',
                    'content': 'Easy recipes and cooking techniques for beginners. Delicious meals don\'t have to be complicated!',
                    'genre': 'Food'
                },
            ]
            
            genres = Genre.objects.all()
            for i, post_data in enumerate(sample_posts_data):
                if i < len(created_users):
                    author = created_users[i]
                else:
                    author = random.choice(created_users)
                    
                try:
                    genre = genres.get(name=post_data['genre'])
                except Genre.DoesNotExist:
                    genre = genres.first()
                
                post, created = Post.objects.get_or_create(
                    title=post_data['title'],
                    defaults={
                        'content': post_data['content'],
                        'author': author,
                        'genre': genre,
                    }
                )
                
                if created:
                    self.stdout.write(f'  ✓ Created post: {post.title}')
                else:
                    self.stdout.write(f'  - Post already exists: {post.title}')
            
            self.stdout.write(
                self.style.SUCCESS('📝 Sample data created successfully!')
            )