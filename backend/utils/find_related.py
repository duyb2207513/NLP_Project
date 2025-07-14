from googlesearch import search

def find_related_links(query, num_results=3):
    related_links = []
    for url in search(query, num_results=num_results, lang="vi"):
        if any(source in url for source in ['vnexpress.net', 'tuoitre.vn', 'vtv.vn', 'moit.gov.vn']):
            related_links.append(url)
    return related_links
