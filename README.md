# WikipediaSQL

Web interface to execute SQL queries against a simplified dataset of the simple english wikipedia.

## Dataset

The simple english wikipedia makes its dataset available through periodical dumps. It offers two formats: XML and SQL files.

Due to preprocessing time saving, this project uses the SQL files. Specifically the files used are:

  * simplewiki-20181101-page.sql:  Base per-page data (id, title, etc)
  * simplewiki-20181101-categorylinks.sql: Wiki category membership link records
  * simplewiki-20181101-pagelinks.sql: Wiki page-to-page link records

### Simplifications

The dataset has been simplified, removing from each table the not interesting columns for our analysis. Too see the dropped columns take a look at 'SQL/clean_data.sql'.

Additionally the link position attribute for each links has been omitted, since it is not possible to derive this information from the SQL files. The only solution to obtain the link position is to parse the raw text of each page in XML format, and that would involve too much developing time.


### Final schema

The final schema after all the steps explained above is as follows:

* **Tables:**
  * page
    * page_id           INT UNSIGNED
    * page_namespace    INT
    * page_title        VARBINARY
    * page_touched      VARBINARY
    * page_latest       INT UNSIGNED
  * categorylinks
    * cl_from           INT UNSIGNED
    * cl_to             VARBINARY
    * cl_timestamp      TIMESTAMP
    * cl_type           ENUM('page','subcat','file')
  * pagelinks
    * pl_from           INT UNSIGNED
    * pl_namespace      INT
    * pl_title          VARBINARY
    * pl_from_namespace INT

For an explanation on each of this fields visit [page](https://www.mediawiki.org/wiki/Manual:Page_table), [categorylinks](https://www.mediawiki.org/wiki/Manual:Categorylinks_table) and [pagelinks](https://www.mediawiki.org/wiki/Manual:Pagelinks_table) table documentation.

### Get the data

To get the data in the exact same format explained above, you can use the 'SQL/ingest.sh' script, that actually downloads, inserts and cleans the data in the database (Tested with MySQL 5.7).

You need to provide the host, username, password and database name of the database you want to use as command line arguments.

Example of use:

``` bash
$ ./ingest.sh mydatabase.mydomain username password database
```

## Endpoints

**Home**
---
Exposes and SQL editor to run queries against the dataset. You only have to type your query in the text area provided and then click on 'Execute' button.

* **Url:**

  `GET | POST` `/`

* **Body:**

``` js
Content-Disposition: form-data; name="query"

select * from page limit 20
```

>The results of the queries are truncated, to prevent loading to much >records. The proper way of doing this would be using pagination, but it >is not trivial to implement for this endpoint. 
>The truncated size is controlled through the 'FETCH_SIZE' parameter.


**Outdated**
---
Like 'home' endpoint, but in this case the query is fixed to the following:

``` sql
SELECT a.page_id, CAST(a.page_title AS CHAR) title, a.page_touched AS referrerDate, b.page_touched AS referredDate
FROM (select * from page where page_id IN (SELECT cl_from FROM categorylinks WHERE lower(CAST(cl_to AS CHAR)) = :category)) AS a
    JOIN
    pagelinks AS p ON a.page_id = p.pl_from
    JOIN
    page AS b ON p.pl_title = b.page_title AND b.page_touched > a.page_touched
ORDER BY (b.page_touched - a.page_touched) DESC
LIMIT 1
```

and you can only specify the ':category' param through the text area provided.

* **Url:**

  `GET | POST` `/outdated`

* **Body:**

``` js
Content-Disposition: form-data; name="category"

living people
```
## Development

The project is developed in Python 3.6, using the Flask web microframework. A makefile is provided to ease the use.

* **Running the project locally:**

``` bash
$ make install
$ make run
```

Note that you will have to set the appropiate environment variables in a .env file, before be able to run the project. A '.env.example' is provided as template.

### Deployment 

The project is deployed in a serverless fashion, using AWS Lambda + AWS API Gateway services and the [zappa framework](https://github.com/Miserlou/Zappa)