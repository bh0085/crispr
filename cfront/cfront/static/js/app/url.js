/**
 * Class CUrl is created o page init replicates the functionality
 * of Pyramid's route_path for URLs that need to be generated in
 * the frontend.
 * 
 */

var CUrl = Backbone.Model.extend(/**@lends CUrl*/{
    initialize:function(routes){
        this.names = routes;
    },
    route_path:function(name, keys){
        keys = keys || {};
        var url = this.names[name];
        if (!url){throw "route name unrecognized: " + name;} 
        _.each(keys,function(v,k){
            url = url.replace(RegExp('{'+k+'}'),v);
        });
        if(  url.indexOf('{') != -1){
            throw "incomplete key replacement for " + name+ " - " + url;
        }
        return url;
    }
});

function encodeURL(theUrl, extraParameters) {
    var extraParametersEncoded = $.param(extraParameters);
    var seperator = theUrl.indexOf('?') == -1 ? "?" : "&";
    return(theUrl + seperator + extraParametersEncoded);
}


function urlExists(url)
{
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();
    return http.status!=404;
}

