# sphinx-notion

`sphinx-notion` is a Sphinx extension that converts manuscripts (reST, etc.) to a Notion API compatible JSON file.

`sphinx-notion` adds `notion` builder.

## Example

* reST: https://github.com/ftnext/sphinx-notion/tree/main/example
* Notion page: https://actually-divan-348.notion.site/sphin-notion-example-index-rst-1dce5fe10a37818098a0fd61578b06d3

## Usage

1. Create your Sphinx documentation
2. Edit `conf.py` to use this extension

```python
extensions = [
    "sphinx_notion",
]
```

3. Run `make notion`

Or other command example:

```
uvx --from Sphinx \
  --with sphinx-notion \
  sphinx-build -M notion source build
```

Optional: Upload a JSON file under `build/notion/` with a [script](https://github.com/ftnext/sphinx-notion/blob/main/upload.py).
