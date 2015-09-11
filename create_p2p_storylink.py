from clint.textui import colored
from tarbell.hooks import register_hook
from tarbell.utils import puts

@register_hook('publish')    
def create_p2p_storylink(site, s3):
    """Create or update a P2P storylink content item when publishing this project"""
    puts("\nAttempting to create P2P storylink for this project ...\n")

    try:
        import p2p
    except ImportError:
        puts(colored.red(
            "The p2p-python package is not installed. Storylink not created.\n"))
        return

    if not is_production_bucket(s3.bucket, site.project.S3_BUCKETS):
        puts(colored.red(
            "Not publishing to production bucket. Skipping storylink creation\n."))
        return

    try:
        p2p_slug = site.project.DEFAULT_CONTEXT['P2P_STORYLINK_SLUG']
    except KeyError:    
        puts(colored.red(
            "P2P_STORYLINK_SLUG not defined in DEFAULT_CONTEXT. Storylink "
            "not created.\n"))
        return

    url = "http://" + s3.bucket

    connection = p2p.get_connection()
    content_item = {
        'slug': p2p_slug,
        'content_item_type_code': 'storylink', 
        'url': url,
        'title': site.project.DEFAULT_CONTEXT['title'],
    }
    created, ci = connection.create_or_update_content_item(content_item)
    if created:
        puts(colored.green(
            "P2P storylink with slug '{slug}' created.\n".format(
                slug=p2p_slug)))
        connection.update_content_item({
            'slug': p2p_slug,
            'content_item_state_code': 'working',    
        })    
        ci['content_item_state_code'] = 'working'
    else:
        puts(colored.green("P2P storylink with slug '{slug}' updated.\n".format(
            slug=p2p_slug)))

    if 'thumbnail_url' not in ci:
        puts(colored.cyan(
            "No thumbnail for storylink.  Be sure to add one in P2P."))


def is_production_bucket(bucket_url, buckets):
    for name, url in buckets.items():
        if url == bucket_url and name == 'production':
            return True

    return False   
