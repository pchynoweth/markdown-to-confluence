import mistune
import os
import textwrap
import yaml

from urllib.parse import urlparse

YAML_BOUNDARY = '---'


def parse(post_path):
    """Parses the metadata and content from the provided post.

    Arguments:
        post_path {str} -- The absolute path to the Markdown post
    """
    raw_yaml = ''
    markdown = ''
    in_yaml = True
    with open(post_path, 'r') as post:
        for line in post.readlines():
            # Check if this is the ending tag
            if line.strip() == YAML_BOUNDARY:
                if in_yaml and raw_yaml:
                    in_yaml = False
                    continue
            if in_yaml:
                raw_yaml += line
            else:
                markdown += line
    front_matter = yaml.load(raw_yaml, Loader=yaml.SafeLoader)
    markdown = markdown.strip()
    return front_matter, markdown


def convtoconf(markdown, front_matter={}):
    if front_matter is None:
        front_matter = {}

    author_keys = front_matter.get('author_keys', [])
    renderer = ConfluenceRenderer(authors=author_keys)
    content_html = mistune.markdown(markdown, renderer=renderer)

    return content_html, renderer.attachments


class ConfluenceRenderer(mistune.Renderer):
    def __init__(self, authors=[]):
        self.attachments = []
        if authors is None:
            authors = []
        self.authors = authors
        self.has_toc = False
        super().__init__(use_xhtml=True)

    def header(self, text, level, raw=None):
        """Processes a Markdown header.

        In our case, this just tells us that we need to render a TOC. We don't
        actually do any special rendering for headers.
        """
        self.has_toc = True
        return super().header(text, level, raw)

    def block_code(self, code, lang):
        return textwrap.dedent('''\
            <ac:structured-macro ac:name="code" ac:schema-version="1">
                <ac:parameter ac:name="language">{l}</ac:parameter>
                <ac:plain-text-body><![CDATA[{c}]]></ac:plain-text-body>
            </ac:structured-macro>
        ''').format(c=code, l=lang or '')

    def image(self, src, title, alt_text):
        """Renders an image into XHTML expected by Confluence.

        Arguments:
            src {str} -- The path to the image
            title {str} -- The title attribute for the image
            alt_text {str} -- The alt text for the image

        Returns:
            str -- The constructed XHTML tag
        """
        # Check if the image is externally hosted, or hosted as a static
        # file within Journal
        is_external = bool(urlparse(src).netloc)
        tag_template = '<ac:image>{image_tag}</ac:image>'
        image_tag = '<ri:url ri:value="{}" />'.format(src)
        if not is_external:
            image_tag = '<ri:attachment ri:filename="{}" />'.format(
                os.path.basename(src))
            self.attachments.append(src)
        return tag_template.format(image_tag=image_tag)
