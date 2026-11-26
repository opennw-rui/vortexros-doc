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
    env = app.env

    def entry(doc):
        metadata = env.metadata.get(doc, {})
        children = [entry(child) for child in env.toctree_includes.get(doc, [])]
        return {
            "doc": doc,
            "title": metadata.get("nav_title") or env.titles[doc].astext(),
            "overview": metadata.get("nav_overview", "概览"),
            "active": doc == page or any(child["active"] for child in children),
            "children": children,
        }

    context["feature_navigation"] = [
        entry(doc) for doc in env.toctree_includes[app.config.root_doc]
    ]


def setup(app):
    app.add_lexer("vortexros-cli", TextLexer)
    app.add_lexer("vortexros-config", TextLexer)
    app.connect("html-page-context", feature_navigation)
