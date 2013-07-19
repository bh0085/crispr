var FileM = Backbone.RelationalModel.extend({
    idAttribute:"url"
})
var FileCollection = Backbone.Collection.extend({model:FileM})
