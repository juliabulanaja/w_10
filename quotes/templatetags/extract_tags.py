from django import template

register = template.Library()


def tag_list(tags):
    return ','.join([str(name) for name in tags.all()])


register.filter('tag_list', tag_list)