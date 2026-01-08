def theme_context(request):
    """
    Add theme-related context to all templates
    """
    theme_mode = 'dark' if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.dark_mode else 'light'
    
    return {
        'theme_mode': theme_mode,
        'SITE_NAME': "Tori's Blog",
        'SITE_DESCRIPTION': 'A modern blog platform inspired by Substack',
    }