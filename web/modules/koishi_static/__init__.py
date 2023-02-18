from flask import Blueprint, render_template

from gh_md_to_html.core_converter import markdown as generate_markdown
from os.path import split as split_path, join as join_paths

URL_PREFIX = '/project/koishi'

ROUTES = Blueprint('koishi_static', '', url_prefix = URL_PREFIX)

MARKDOWN_DIRECTORY = join_paths(split_path(__spec__.origin)[0], 'markdowns')

def create_markdown(path):
    with open(path, 'r') as file:
        content = file.read()
        markdown = generate_markdown(content)
    
    return markdown


TERMS_OF_SERVICE_MARKDOWN = create_markdown(join_paths(MARKDOWN_DIRECTORY, 'terms_of_service.md'))
PRIVACY_POLICY_MARKDOWN = create_markdown(join_paths(MARKDOWN_DIRECTORY, 'privacy_policy.md'))


@ROUTES.route('/terms_of_service')
def get_terms_of_service():
    return render_template(
        'koishi_static.html',
        title = 'Terms of Service',
        markdown = TERMS_OF_SERVICE_MARKDOWN,
    )


@ROUTES.route('/privacy_policy')
def get_privacy_policy():
    return render_template(
        'koishi_static.html',
        title = 'Privacy Policy',
        markdown = PRIVACY_POLICY_MARKDOWN,
    )
