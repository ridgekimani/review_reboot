__author__ = 'm'

from django_assets import Bundle, register

base_js = Bundle('js/select.min.js',
                 'js/autosize.min.js',
                 "js/icheck.js",
                 # 'js/scroll.min.js',
                 # 'js/calendar.min.js',
                 'js/feeds.min.js',
                 # 'js/toggler.min.js',
                 # 'js/functions.js',
                 filters="jsmin",
                 output="dist/base.js")

core_js = Bundle('js/jquery.min.js',
                 "js/bootstrap.min.js",
                 filters="jsmin",
                 output="dist/core.js")

base_css = Bundle('css/bootstrap.min.css',
                  'css/animate.min.css',
                  'css/font-awesome.min.css',
                  'css/form.css',
                  'css/calendar.css',
                  'css/style.css',
                  'css/icons.css',
                  'css/generics.css',
                  'scss/restaurant.css',
                  filters="cssmin",
                  output="dist/base.css")

# javascript
register("base-js", base_js)
register("core-js", core_js)

# styles
register("basecss", base_css)
