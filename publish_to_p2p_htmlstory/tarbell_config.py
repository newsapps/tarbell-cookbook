from clint.textui import colored

from tarbell.hooks import register_hook
from tarbell.utils import puts

import p2p

def is_production_bucket(bucket_url, buckets):
    for name, url in buckets.items():
        if url == bucket_url and name == 'production':
            return True

    return False

@register_hook('publish')
def p2p_publish(site, s3):
    if not is_production_bucket(s3.bucket, site.project.S3_BUCKETS):
        puts(colored.red(
            "\nNot publishing to production bucket. Skipping P2P publiction."))
        return

    content = _get_published_content(site, s3)
    content = content.encode('utf-8')
    context = site.get_context(publish=True)

    p2p_slug = context['p2p_htmlstory_slug']
    try:
        title = context['headline']
    except KeyError:
        title = context['title']
    p2p_conn = p2p.get_connection()
    content_item = {
        'slug': p2p_slug,
        'content_item_type_code': 'htmlstory',
        'title': title,
        'body': content,
    }
    p2p_conn.create_or_update_content_item(content_item)

    puts("\n" + colored.green("Published to P2P with slug {}".format(p2p_slug)))


def _get_published_content(site, s3):
    template = site.app.jinja_env.get_template('htmlstory.html')
    context = site.get_context(publish=True)
    return template.render(**context)
