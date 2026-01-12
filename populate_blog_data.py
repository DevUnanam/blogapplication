#!/usr/bin/env python
"""
Blog Data Population Script

This script populates your blog with sample users and articles.
Run this to quickly set up your blog with realistic test data.

Usage:
    python populate_blog_data.py [options]

Options:
    --users N       Number of users to create (default: 15)
    --articles N    Number of articles to create (default: 50)
    --clear         Clear existing data before populating
    --help          Show this help message

Examples:
    python populate_blog_data.py
    python populate_blog_data.py --users 20 --articles 100
    python populate_blog_data.py --clear --users 15 --articles 50
"""

import os
import sys
import django

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tori_blog.settings')
django.setup()

from django.core.management import call_command


def main():
    print("🌱 Blog Data Population Script")
    print("=" * 40)

    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Populate blog with sample data')
    parser.add_argument('--users', type=int, default=15, help='Number of users to create')
    parser.add_argument('--articles', type=int, default=50, help='Number of articles to create')
    parser.add_argument('--clear', action='store_true', help='Clear existing data')

    args = parser.parse_args()

    print(f"Users to create: {args.users}")
    print(f"Articles to create: {args.articles}")
    print(f"Clear existing data: {'Yes' if args.clear else 'No'}")
    print("-" * 40)

    try:
        # Install Faker if not installed
        try:
            import faker
        except ImportError:
            print("Installing Faker library...")
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Faker==26.0.0'])
            print("✓ Faker installed successfully")

        # Run the population command
        call_command('populate_data',
                    users=args.users,
                    articles=args.articles,
                    clear=args.clear)

        print("\n🎉 Population completed successfully!")
        print("\nYou can now:")
        print("1. Run the Django server: python manage.py runserver")
        print("2. Visit your blog and see the populated content")
        print("3. Login with any created user (password: 'test')")

    except Exception as e:
        print(f"\n❌ Error during population: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you've run: python manage.py migrate")
        print("2. Ensure all requirements are installed: pip install -r requirements.txt")
        print("3. Check that your database is accessible")

        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())