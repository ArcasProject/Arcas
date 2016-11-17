Scraping IEEE Xplore Search Gateway
===================================

Parameters
----------
Some of the syntax, mainly the one being used currently for this project,
for querying the IEEE Xplore Search Gateway is as follow:

|Parameter| Description                 | Boolean query field|
|---------|-----------------------------|--------------------|
| au      |Terms to search for in Author|Author              |
| ti      |Terms to search for in Document Title|"Document Title"|
| ab      |Terms to search for in Abstract|Abstract          |
| py      |Terms to search for in Publication Year|"Publication Year"|
| hc      |Number of records to fetch. Default: 25; Maximum: 1000|   |

For further search parameters available in IEEE Xplore see visit the
official site: http://ieeexplore.ieee.org/gateway/.

Return Structure
----------------

IEEE Xplore returns the articles in an XML format. Though XML format vary
depending on the website. Thus here the structure of the XML answers is
seen. 

        -<root>
            -<totalfound> </totalfound>
            -<totalsearched> </totalsearched><dimensions>
            -<document> 
                <rank> </rank>
                <title> </title>
                <authors> </authors>
                <affiliations> </affiliations>
                <controlledterms>
                    <term> </term>
                    <term> </term>
                    <term> </term>
                </controlledterms>
                <thesaurusterms>                      
                    <term> </term>
                    <term> </term>
                    <term> </term>
                 </thesaurusterms>
                 <pubtitle> </pubtitle>
                 <punumber> </punumber>
                 <pubtype> </pubtype>
                 <publisher> </publisher>
                 <volume> </volume>
                 <issue> </issue>
                 <py> </py>
                 <spage>1281</spage>
                 <epage>1290</epage>
                 <abstract> </abstract>
                 <issn> </issn>
                 <htmlFlag>1</htmlFlag>
                 <arnumber> </arnumber>
                 <doi> </doi>
                 <publicationId> </publicationId>
                 <partnum> </partnum>
                 <mdurl> </mdurl>
                 <pdf> </pdf>
            </document>
        </root>