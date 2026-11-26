from pygments.lexers.special import TextLexer

project = "VortexROS 用户手册"
release = "v0.1.0-dev"
language = "zh_CN"
root_doc = "index"
extensions = ["myst_parser", "sphinx_rtd_theme"]
exclude_patterns = ["**/README.md"]
templates_path = ["_templates"]

html_theme = "sphinx_rtd_theme"
html_title = "VortexROS 用户手册"
html_baseurl = "https://opennw-rui.github.io/vortexros-doc/"
html_static_path = ["_static"]
html_css_files = ["manual.css"]
html_show_sourcelink = False
html_copy_source = False


def feature_navigation(app, page, template, context, doctree):
    tree = app.env.toctree_includes
    titles = app.env.titles

    def leaves(doc):
        children = tree.get(doc, [])
        if not children:
            yield doc, titles[doc].astext()
        for child in children:
            yield from leaves(child)

    context["feature_navigation"] = [
        (titles[category].astext() if tree.get(category) else "", list(leaves(category)))
        for category in tree[app.config.root_doc]
    ]


def setup(app):
    app.add_lexer("vortexros-cli", TextLexer)
    app.add_lexer("vortexros-config", TextLexer)
    app.connect("html-page-context", feature_navigation)
