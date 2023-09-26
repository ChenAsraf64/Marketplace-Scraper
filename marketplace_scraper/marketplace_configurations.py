# This dictionary hold as a key of the marketplace name and holding as value a list of URL 
# search format and CSS selector for extrac data
search_url_dictionary = {
    'ebay' : [
        'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={search_word}&_sacat=0', #URL template for search result [0]
        '.s-item__link::attr(href)', #CSS selector for extract individual item URL [1]
        '.pagination__next::attr(href)', #CSS selector for extract next page URL [2]
        'https://vi.vipr.ebaydesc.com/ws/eBayISAPI.dll?item={item_id}', #URL template to fetch desciption of specific item [3]
        'h1 span::text', #CSS selector for item title [4]
        '.x-price-primary span::text', #CSS selector for item price [5]
        '.ux-image-carousel-item img::attr(src)', #CSS selector for item primary image [6]
        '.ux-layout-section__textual-display--itemId .ux-textspans--BOLD::text' #CSS selector for specific item number [7]
    ]
}
