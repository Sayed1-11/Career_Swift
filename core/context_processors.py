def show_seeker_link(request):
    show_link = True  # Default to showing the link

    # Check if the current view is not SeekerView (or any other view where you want to exclude the link)
    if 'jobs' not in request.resolver_match.func.__globals__:
        show_link = False

    return {'show_seeker_link': show_link}