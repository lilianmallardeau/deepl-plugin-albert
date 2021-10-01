# Deepl plugin for Albert launcher

Plugin to use Deepl translator with Albert launcher

## How to setup
First, a Deepl API key is needed. Create an account on the [Deepl website](https://www.deepl.com/) and subscribe for the [Deepl API Free subscription](https://www.deepl.com/pro-api).

Once you've got your key, clone this repo to the Albert `modules` folder and edit the configuration file:
```
cd ~/.local/share/albert/org.albert.extension.python/modules/
git clone https://github.com/lilianmallardeau/deepl-plugin-albert.git deepl_translate
nano deepl_translate/parameters.env
```

Put your API key in the `DEEPL_API_KEY` variable.

In case you use the Pro (paid) version of the API, change the variable `DEEPL_SUBSCRIPTION` to `pro` (the base URL for the API is not the same for the free API and the Pro API).

You can also change the triggers for the plugin if you want, by changing the `__triggers__` variable in `__init__.py`.

You may need to restart Albert for it to load the plugin. Don't forget to activate the module in the Albert settings, under "Python Extensions".

## How to use
```
deepl <target-lang> <text>
deepl <src-lang:target-lang> <text>
```

For example:
```
deepl fr Hello world!
deepl en:fr Hello world!
```

When the source language is not specified, Deepl will detect it.
Once the translation is shown, pressing Enter will copy it to the clipboard.


## Requirements
[`python-dotenv`](https://pypi.org/project/python-dotenv/) Python package. It can be installed from [Pypi](https://pypi.org/project/python-dotenv/).