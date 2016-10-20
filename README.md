django-knockout
===

**[django-knockout](//github.com/AntycSolutions/django-knockout)** makes it super easy to use [knockout.js](//knockoutjs.com/) with your [Django](//www.djangoproject.com/) models. It's great for project with objects that have lots of different models, or models with lots of different fields, or both. It can be used in both prototyping complex applications and directly in the templates of simple ones. Supports forms and formsets via [Knockout pre-rendered](//github.com/ErikSchierboom/knockout-pre-rendered). Supports [Django Rest Framework](//django-rest-framework.org) and [jQuery](//jquery.com) by default, but these can be disabled.

Forked from [django-knockout-modeler](//github.com/Miserlou/django-knockout-modeler).

### Requirements
* [Python](//python.org) 2.7 or 3.4+
* [Django](//djangoproject.com) 1.8
* [Knockout](//knockoutjs.com) 3.3+

Optional
* [Knockout pre-rendered](//github.com/ErikSchierboom/knockout-pre-rendered) 0.5+
* [Django Rest Framework](//django-rest-framework.org) 3.3+
* [jQuery](//jquery.com) 2.1+

### Preview
**django-knockout** (with Django Rest Framework) turns this:

```python
# models.py
class MyObject(models.Model):
    my_number = models.IntegerField()
    my_name = models.CharField()

# views.py
myobject_class = MyObject

# serializers.py
class MyObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MyObject
        fields = '__all__'

# api.py
class MyObjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MyObjectSerializer
    metadata_class = metadata.KnockoutMetadata
    queryset = models.MyObject.objects.all()
    
# urls.py
router = routers.DefaultRouter()
router.register(r'myobjects', api.MyObjectViewSet, 'myobject')
urlpatterns += urls.url(r'^api/', urls.include(router.urls)),
```

Into this:

```javascript
var MyObjectViewModel = function (data) {
    var self = this;
    self.my_number = ko.observable(data.my_number);
    self.my_name = ko.observable(data.my_name);
}

var MyObjectListViewModel = function(data) {
    var self = this;
    self.myobjects = ko.observableArray(data);
}

var myobject_data = $.getJSON("/app/api/myobjects/").then(function(data) {
    var ko_data = ko.mapping.fromJS(data)();
    return new MyObjectListViewModel(ko_data);
});

function ko_bind_myobjectviewmodel() {
    var element = document.body;
    person_data.done(function(view_model) {
        ko.applyBindings(view_model, element);
    });    
}

person_options.done(ko_bind_myobjectviewmodel);
```

With this!

```html+django
{# template #}
{% knockout myobject_class %}
```

Quick Start
---

0. Install django-knockout 
    via git (and then make sure the subfolder knockout is available to your PYTHONPATH)
    ```bash
    git clone github.com/AntycSolutions/django-knockout
    ```
    ~~via pip~~
    // TODO (not currently on pip)
    ```bash
    pip install django-knockout
    ```

1. Add 'knockout' to your INSTALLED_APPS setting:

    ```python
    # settings.py
    INSTALLED_APPS = (
      ...
      'knockout',
      # django rest framework, can be disabled
      'restframework',
    )
    ```

2. Include knockout.js in your HTML:

    ```html+django
    {# template #}
    <script type='text/javascript' src='//cdnjs.cloudflare.com/ajax/libs/knockout/3.3.0/knockout-min.js'></script>
    <script type='text/javascript' src='//cdnjs.cloudflare.com/ajax/libs/knockout.mapping/2.4.1/knockout.mapping.js'></script>
    {# Optionally needed if you're using forms/formsets #}
    <script type='text/javascript' src='//cdnjs.cloudflare.com/ajax/libs/knockout-pre-rendered/0.5.0/knockout-pre-rendered.min.js'></script>
    {# jQuery, can be disabled #}
    <script type='text/javascript' src='//code.jquery.com/jquery-3.1.1.js'></script>
    ```

4. Knockout your QuerySet:

    ```html+django
    {# template #}
    {% load knockout_tags %}
    <script type="text/javascript">
        {% knockout my_objects %}
    </script>
    ```

6. Loop over your bound data like so:

    ```html+django
    {# template #}
    <div data-bind="foreach: myobjects">
        My Name: <span data-bind="value: my_name"></span>
        My Number: <span data-bind="value: my_number"></span>
    </div>
    ```

Simple Usage
---

**django-knockout** can be used directly in templates to generate knockout view models. 

To get just the list view model, if you prefer to load your data from API's, like this:

```html+django
{# template #}
{% knockout_list_view_model myobject_class %}
```

or if you don't need a list view model just a regular view model:

```html+django
{# template #}
{% knockout_view_model myobject_class %}
```

And even just the bindings:

```html+django
{# template #}
{% knockout_bindings myobject_class %}
```

If you'd like to output the list utils (see below for more information):

```html+django
{# template #}
{% knockout_list_utils myobject_class %}
```

Progammatic Usage
---

First, import it!

```python
from knockout import ko
```

To get the whole template, you can do this:

```python
ko_string = ko.ko(MyObject)
```

Just the List View Model

```python
ko_list_view_model_string = ko.ko_list_view_model(MyObject)
```

Just the View Model

```python
ko_view_model_string = ko.ko_view_model(MyObject)
```

list utils (see below for more information):

```python
ko_list_utils_string = ko.ko_list_utils(MyObject)
```

Custom fieldsets are also allowed (see Access Control):
```python
from knockout import forms

class MyObject():
    ...
    def knockout_fields(self):
        return ['my_name', 'my_number', ...]

myobject_knockout_model_form = MyObjectKnockoutModeLForm(forms.KnockoutModelForm)

ko_string = ko(MyObject, knockout_model)
// TODO, finish documentation for KnockoutModelForm
```

Access Control
---

If you don't want to expose your entire model to Knockout, you can define a function in your model:
// currently just forms, TODO: make knockout_fields work not just for forms
```python
def knockout_fields(self):
    return ['id', 'my_name', 'my_number', ...]
```

Sorting
----------

django knockout provides some convenience methods (via `knockout_list_utils`/`ko_list_utils`) for manipulating your arrays:

```javascript
    self.addMyObjectViewModel = function(data) {
        self.persons.push(new MyObjectViewModel(data));
    };

    self.createMyObjectViewModel = function(data) {
        return new MyObjectViewModel(data);
    };

    self.removeMyObjectViewModel = function(data) {
        self.persons.remove(data);
    };

    self.destroyMyObjectViewModel = function(data) {
        self.persons.destroy(data);
    };

    self.deleteMyObjectViewModel = function(data) {
        var index = self.persons.indexOf(data);
        self.persons()[index].DELETE(true);
    }
```

* See [here](http://knockoutjs.com/documentation/observableArrays.html) for what the destroy function is for
* The data parameter for add/create is optional
* The delete function is for formsets

for sorting your data (see below for changing the comparator):

```javascript
self.sortMyObjectViewModelsAsc = function() {
    self.myobjects.sort(function(a, b) {
        var a_comparator = a.id();
        var b_comparator = b.id();
        if (!a_comparator) { a_comparator = undefined; }
        if (!b_comparator) { b_comparator = undefined; }
        var result = a_comparator>b_comparator?-1:a_comparator<b_comparator?1:0;

        return result;
    });
};

self.sortMyObjectViewModelsDesc = function() {
    self.myobjects.sort(function(a, b) {
        var a_comparator = a.id();
        var b_comparator = b.id();
        if (!a_comparator) { a_comparator = undefined; }
        if (!b_comparator) { b_comparator = undefined; }
        var result = a_comparator<b_comparator?-1:a_comparator>b_comparator?1:0;

        return result;
    });
};
```

Include this in your template:

```html+django
{# template #}
<button data-bind='click: sortMyObjectViewModelsAsc'>Sort Asc</button>
<button data-bind='click: sortMyObjectViewModelsDesc'>Sort Desc</button>
```

By default, it will use the object's 'id' field, but you can also define your own comparator like so:

```python
def comparator(self):
    return 'my_name'  # or whichever field
```

If you don't define a comparator, 'id' must be in your knockout_fields.

Multi-Model Support
----------

django-knockout is all ready set up to be used with multiple types of data at the same time, as bindings can happen to specific objects:

```javascript
function ko_bind() {
    var element_id = "myobjectviewmodel";
    var element = document.getElementById(element_id);
    
    ko.applyBindings(new MyObjectListViewModel(), element);
}
ko_bind();
```

which means that you somewhere in your HTML template, you will need to have an object with that id, like so:

```html+django
{# template #}
<div id="myobjectviewmodel">
    <div data-bind="foreach: myobjects">
        User <span data-bind="value: my_name"></span> is number <span data-bind="value: my_number"></span>.
    </div>
</div>
```

and add the paramter to the `knockout` tag:

```html+django
{# template #}
{% knockout myobject_class element_id="myobjectviewmodel" %}
```

This is handy for prototyping, but more advanced applications may want to use the [Master View Model](http://stackoverflow.com/a/9294752/1135467) technique instead.
// TODO: still relevant?

Custom Data Support
---------

Is django-knockout using the wrong url? Pass it into `knockout`/`ko` or `knockout_bindings`/`ko_bindings`:

```html+django
{# template #}
{% url 'app:myobject-list' as myobject_list_url %}
{% knockout myobject_class url=myobject_list_url %}
```

```python
ko(MyObject, url='/app/api/myobjects')
```
