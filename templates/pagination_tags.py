from django import template
from django.core.paginator import Paginator
register = template.Library()

@register.simple_tag(takes_context=True)
def render_pagination(context, page_obj):
    # Get the request object from the context
    request = context['request']

    # Get the current page number
    current_page = page_obj.number

    # Create a Paginator object using the page_obj queryset
    paginator = Paginator(page_obj.object_list, per_page=10)

    # Render the pagination HTML code
    return paginator.get_bootstrap4_html(request, current_page)
