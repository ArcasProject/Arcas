Scraping ArXiv Api
==================

Parameters
----------
|Parameter| Description                 |
|---------|-----------------------------|
| au      |Author                  |
| ti      |Title                   |
| ab      |Abstract                |
| co      |Comment                 |
| jr      |Journal Reference       |
| cat     |Subject Category        |
| rn      |Report Number           |
| id 	  |Id (use id_list instead)|
| all 	  |All of the above        |
|max_results| |

For further details of the ArXiv Api and search arguments visit the official
site: https://arxiv.org/help/api/index.

Return Structure
----------------

ArXiv Api returns the articles in an XML format. Though XML format vary
depending on the website. Thus here the structure of the XML answers is
seen.
        
        -<root>
            -<title> The title of the feed containing a canonicalized 
                        query string.
            -<id> A unique id assigned to this query.
            -<updated> The last time search results for this query were 
                        updated. Set to midnight of the current day.
            -<link> A url that will retrieve this feed via a GET request.
            -<opensearch:totalResults> The total number of search results
                                       for this query.
            -<opensearch:startIndex> The 0-based index of the first returned 
                                     result in the total results list.
            -<opensearch:itemsPerPage> The number of results returned. 
            -<element>
                -<title> The title of the article.
                -<id> A url http://arxiv.org/abs/id
                -<published> The date that version 1 of the article was submitted.
                -<updated> The date that the retrieved version of the article
                           was submitted. Same as <published> if the retrieved 
                           version is version 1.
                -<summary> The article abstract.
                -<author> One for each author. Has child element <name> 
                          containing the author name.
                -<link> Can be up to 3 given url's associated with this article.
                -<category> The arXiv or ACM or MSC category for an article if present.
                -<arxiv:primary_category> The primary arXiv category.
                -<arxiv:comment> The authors comment if present.
                -<arxiv:affiliation> The author's affiliation included as 
                                     a subelement of <author> if present.
                -<arxiv:journal_ref> A journal reference if present.
                -<arxiv:doi> A url for the resolved DOI to an external 
                             resource if present. 
             -/<element>
        -/<root>
        
**Tips (from the official wedsite):
    - play nice and incorporate a 3 second delay in your code
    -  max_results) is limited to 30000 **