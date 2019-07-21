from tool.text import text_join, text_replace, code_files, code_search, html_files, html_search, doc_files, doc_search, text_search
from tool.shell import redact_css


def text_code_files_test():
    return text_join(code_files())


def text_code_search_test():
    return code_search(['def ', 'module'])


def text_css_filter_test():
    text = '<link href="/static/css/guide.css?time=July 4, 2019, 8:42 a.m.">\nOutput this'
    return redact_css(text)


def text_doc_files_test():
    return text_join(doc_files())


def text_doc_search_test():
    # return text_search(['h1'])

    text = doc_search(['Seaman','shrinkingworld'])
    return text


def text_html_files_test():
    return text_join(html_files())


def text_html_search_test():
    return html_search(['h1'])


def text_replace_test():
    return text_replace('Four score and seven years', 'score', 'generations')


def text_search_test():
    return text_search(['h1'])
