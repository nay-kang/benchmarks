## I want to know the difference in sqlite that query direct with large text and query with hashed short text.  
I also add indexed hashed short text and primary key togather with large text query.  
here is the execute result in seconds
| | direct query | hashed short text | indexed hashed text | large text togather with primary key |
| :--- | :--: | :--: | :--: | ---: |
| prepare table | 432(100%) | 443(102%) | 444(102%) | 445(103%) |
| test run | 1321(100%) | 1217(92%) | 443(33%) | 447(33%) |

## Observations
* compare the **short text** with **large text** there is no significant performance change.only 92%
* the prepare time are almost the same.**large text togather with primary key** has no defference with **direct query**,so the 3% is tolerance. so whether doing hash or indexing, the timing is negligible.
* indexing text or int has no difference in sqlite in query