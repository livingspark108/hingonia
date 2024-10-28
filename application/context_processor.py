def device_type(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    is_safari = 'safari' in user_agent and 'chrome' not in user_agent
    is_pc = any(os in user_agent for os in ['windows', 'linux', 'macintosh'])

    return {
        'is_safari': is_safari,
        'is_pc': is_pc,
    }