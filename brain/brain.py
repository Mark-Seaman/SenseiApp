from django.utils.timezone import now
from os import listdir
from os.path import exists, isdir, isfile, join
from subprocess import Popen, PIPE
from sys import version_info
from tool.shell import shell_pipe


# Read document as HTML
def document_html(path):
    return markdown_to_html(read_markdown(path))


# Create a list of documents (doc, title)
def doc_list(path):

    def doc_entry(path, f):
        return document_title(join(path, f)), f

    return [doc_entry(path, f) for f in list_files(path)]


# Find the path to the requested document
def doc_path(doc):
    return join('Documents', doc)


# Redirect to an x for any directory
def doc_redirect(doc):
    while doc.endswith('/'):
        doc = doc[:-1]
    path = doc_path(doc)
    if isdir(path):
        if exists(join(path, 'x')):
            return '/%s/x' % doc
        if exists(join(path, 'x.md')):
            return '/%s/x' % doc
        return '/%s/Files' % doc
    if not exists(path) and not exists(path + '.md'):
        return '/%s/Missing' % doc


# Extract the title from the file text
def document_title(doc):
    text = read_markdown(doc)
    return text.split('\n')[0][2:]


# List the file as hyperlinks to documents
def list_files(path):

    def file_entry(path,f):
        if isdir(doc_path(join(path, f))):
            return "%s/" % f
        else:
            if f != '.DS_Store':
                return f

    files = sorted(listdir(doc_path(path)))
    return [file_entry(path, f) for f in files]


# Convert markdown text to HTML
def markdown_to_html(markdown, image_path='/static/images'):

    def fix_images(text, image_path):
        return text.replace('](img/', '](%s/' % image_path)

    markdown = fix_images(markdown, image_path)
    return shell_pipe('pandoc', markdown)


# Return context settings for the views
def page_settings(**kwargs):
    kwargs['header'] = dict(title='My Notes', subtitle=kwargs.get('title'))
    kwargs['time'] = now()
    return kwargs


# Read the specific document
def read_markdown(doc):
    path = doc_path(doc)
    if exists(path) and isfile(path):
        try:
            return open(path).read()
        except:
            return 'Document is corrupted (doc=%s)' % path
    else:
        return 'No DOCUMENT Found, %s' % doc


# Read the document formatted as HTML
def render_doc(doc):
    path = doc_path(doc)
    if not exists(path) and exists(path + '.md'):
        doc = doc + '.md'
    return document_html(doc)

