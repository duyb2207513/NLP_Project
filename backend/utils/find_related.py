from googlesearch import search


def find_related_links(query, num_results=3):
    related_links = []
    try:
        print(" Đang tìm kiếm với từ khoá:", query)
        for url in search(query, num_results=num_results, lang="vi"):
            # print(" Tìm thấy URL:", url)  # dòng này giúp debug
            # if any(source in url for source in ['baomoi.com','vnexpress.net', 'tuoitre.vn', 'vtv.vn', 'moit.gov.vn','thanhnien.vn']):
            related_links.append(url)
    except Exception as e:
        print(" Lỗi:", e)
    return related_links

print(find_related_links("bão Yagi"))