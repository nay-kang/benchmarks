result first

    Python:39ms
    PHP:26ms
    Java:18ms
    GO:15ms

now we see what we do about this

* first we read items that has relative to the one user from mysql
* than we fetch relative items per item.one item has 100 relative item.and read from mongodb
* finally we loop this items.calc per item score.and rank with score.just simple two for loop.and many hashmap get and set


because the item relation calc by python.so first mind I want to use python to port the api.after some research.I use gunicorn with gevent and flask for simple rest api framework.the empty api request is under 1ms.so that is OK.I thought some db fetch and rank will very fast.then I code about that.but after finish coding.the result is high to 40ms while the user has relative to about 150 items.
So I do a lot search to optimize python code.some works like local method call than reference method call.mongodb batchsize.but some dosen't not work.eg: try pypy interpreter not work and increase more time to response.try cpython and use cdef for variable type.not work.the time is the same.and I already used anaconda with numpy.so the standard CPython is a little slower.

Now I have to try golang.but as I previous experience.I'am not 100% sure that golang will the fastest.empty run great.fetch from mysql great.fetch from mongodb bad.very bad.I search for some golang profile tool.not so much.choose one,pprof,and generate pdf.but I got no why that mongodb so slow.the mongo-golang-driver is short of document.I search a lot still not find how to change cursor.batchSize .

Then I decide to take a look at php.that's very quickly for coding php.install some dependency.all works fine.and speed is faster than PHP.But not satisfied my goal

I want give spring boot a try.the spring guide is perfect.First got an example to quick start.empty run also perfect.It seems all framework empty run is great now.and fetch data from mysql.speed is ok.the code is very easy.then fetch from mongodb.this got a little hard work.I searched an old mongodb java doc.when find the new document.I figure out how to use find $in.but the result is not right.continue research.spring boot log allow mongo output query log.that is very clear.collection not right.anonation that.the result is right.then benchmark.OMG! it's is too slow.not slow than golang.but as slow as python.so I need profile java too.that's easy.visualVM show every request I made.and trace every method call.very clear.the performance bottelneck is BSON document convert.I try to change int array in mongodb to string with comma split.benchmark again.perfect!under 20ms.

So I change other language adapt for mongodb datatype change.re benchmark every language.the result shows above.almost every language gain from this datatype change.
