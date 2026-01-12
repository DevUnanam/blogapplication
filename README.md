# Tori's Blog - Modern Django Blog Platform

A beautiful, modern blog platform inspired by Substack, built with Django and styled with the iconic SpongeBob SquarePants color scheme! 🧽

## 🌟 Features

### 🔐 User Authentication
- User registration, login, and logout
- Custom user profiles with avatars and bio
- Follow/unfollow system between users

### 📝 Blog Posts
- Create, edit, and delete posts (author permissions)
- Rich text content with excerpts
- Featured images for posts
- 15 predefined genres/categories
- Public posts readable by everyone

### 💬 Interactive Comments
- Nested comment system with replies
- Like/unlike posts and comments
- Real-time interaction counters
- User avatars and timestamps

### 🎨 Modern UI/UX
- SpongeBob-inspired color scheme (Yellow #FFD90F, Brown #6B4F1D)
- Fully responsive design (mobile-first)
- Dark/Light mode toggle with user preferences
- Smooth animations and transitions
- Beautiful card layouts and gradients

### 🚀 Advanced Features
- Following feed for subscribed authors
- User profiles with post history and stats
- Genre-based post filtering
- Pagination for better performance
- AJAX interactions for likes and follows
- Search and discovery features

## 🎨 Design Philosophy

The design is inspired by SpongeBob SquarePants with:
- **Primary Yellow (#FFD90F)**: Bright, cheerful, and attention-grabbing
- **Brown (#6B4F1D)**: Warm, reliable, and readable
- **Light variants**: For subtle backgrounds and hover states
- **Dark mode**: Complete theme with proper contrast ratios

## 🛠 Tech Stack

- **Backend**: Django 5.0.6
- **Frontend**: Tailwind CSS + Vanilla JavaScript
- **Database**: PostgreSQL (configurable to SQLite for development)
- **Images**: Pillow for image handling
- **Authentication**: Django's built-in auth system
- **Deployment**: Whitenoise for static files

## 📦 Installation & Setup

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd blogapplication

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration (optional - defaults to SQLite)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=tori_blog
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Set up blog with initial genres and optional sample data
python manage.py setup_blog --create-superuser --create-sample-data

# Or just create genres:
python manage.py setup_blog
```

### 4. Populate with Sample Data (Optional)

For testing and development, you can populate your blog with realistic sample data:

```bash
# Install Faker library for generating sample data
pip install Faker==26.0.0

# Populate with 15 users and 50 articles (default)
python manage.py populate_data

# Custom amounts
python manage.py populate_data --users 20 --articles 100

# Clear existing data and repopulate
python manage.py populate_data --clear --users 15 --articles 50

# Alternative: Use the convenient Python script
python populate_blog_data.py
python populate_blog_data.py --users 20 --articles 75
```

This will create:
- **15 diverse users** with realistic profiles and bios
- **50 articles** across all genres with engaging content
- **Social interactions**: follows, likes, and comments
- **Varied timestamps**: Content spread over the last 6 months

All generated users have the password `test` for easy testing.

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see your blog in action! 🎉

## 📋 Pre-configured Genres

The setup command creates these 15 genres:

1. **Sports** - Sports news, analysis, and personal stories
2. **Comedy** - Funny stories, jokes, and humorous content  
3. **Technology** - Tech news, tutorials, and innovation
4. **Politics** - Political analysis and current affairs
5. **Lifestyle** - Life tips, habits, and personal development
6. **Relationships** - Love, dating, family, and friendships
7. **Finance** - Money management, investing, and economics
8. **Education** - Learning, teaching, and academic content
9. **Health** - Wellness, fitness, and medical information
10. **Travel** - Travel guides, experiences, and adventures
11. **Entertainment** - Movies, music, books, and pop culture
12. **Food** - Recipes, restaurant reviews, and culinary stories
13. **Religion** - Faith, spirituality, and religious discussions
14. **Personal Stories** - Life experiences and personal narratives
15. **Opinion** - Editorial content and personal viewpoints

## 🎯 Usage Guide

### For Writers

1. **Register/Login**: Create your account with a unique username
2. **Setup Profile**: Add your bio, avatar, location, and website
3. **Write Posts**: Click "Write" to create your first post
4. **Choose Genre**: Select the most appropriate category
5. **Add Images**: Upload a featured image to make your post stand out
6. **Publish**: Share your story with the community

### For Readers

1. **Browse Posts**: Explore the homepage for latest content
2. **Filter by Genre**: Use genre buttons to find specific types of content
3. **Follow Authors**: Follow writers whose content you enjoy
4. **Engage**: Like posts and comments, reply to discussions
5. **Create Account**: Join the community to interact and write

### For Developers

The codebase follows Django best practices:

- **Models**: Clean, well-documented model definitions in `blog/models.py`
- **Views**: Class-based views with proper permissions in `blog/views.py`
- **Templates**: Reusable components in `templates/partials/`
- **Static Files**: Organized CSS/JS in `static/`
- **Management Commands**: Custom commands in `blog/management/commands/`

## 🔧 Customization

### Themes and Colors

Edit the Tailwind configuration in `templates/base.html`:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'sponge-yellow': '#FFD90F',  // Change primary color
                'sponge-brown': '#6B4F1D',   // Change secondary color
                // Add your custom colors
            }
        }
    }
}
```

### Adding Features

The modular structure makes it easy to extend:

- Add new models in `blog/models.py`
- Create new views in `blog/views.py` 
- Add URL patterns in `blog/urls.py`
- Create new templates in `templates/blog/`
- Add JavaScript functionality in `static/js/main.js`

## 🚀 Production Deployment

### Environment Setup

1. Set `DEBUG=False` in production
2. Configure proper database settings
3. Set up media file serving (AWS S3, etc.)
4. Configure email backend for notifications
5. Set secure session and CSRF settings

### Static Files

The project uses Whitenoise for static file serving:

```bash
python manage.py collectstatic
```

### Security

- Change `SECRET_KEY` to a secure random string
- Configure `ALLOWED_HOSTS` for your domain
- Set up HTTPS in production
- Configure database with strong passwords

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🧽 Credits

- Inspired by Substack's clean design philosophy
- Color scheme inspired by SpongeBob SquarePants
- Built with love using Django and Tailwind CSS
- Icons by Font Awesome

---

**Ready to start your blogging journey?** Run the setup command and share your first story! 🌟

```bash
python manage.py setup_blog --create-superuser --create-sample-data
python manage.py runserver
```

*"I'm ready! I'm ready! I'm ready to blog!"* - SpongeBob (probably) 🧽