def device_type(request):
    return {
        'is_mobile': request.user_agent.is_mobile,
        'is_tablet': request.user_agent.is_tablet,
        'is_touch_capable': request.user_agent.is_touch_capable,
        'is_pc': request.user_agent.is_pc,
        'is_bot': request.user_agent.is_bot,
        'is_safari': 'Safari' in request.user_agent.browser.family,
    }