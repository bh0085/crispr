//basic setup for the crispr app

Backbone.emulateHTTP = true;

_.templateSettings = {
  interpolate : /\{\{(.+?)\}\}/g
};


exceptions = {
    nospacers:{"message":"no spacers in input sequence"}
}

APP ={}
