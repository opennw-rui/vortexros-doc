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
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
    "titles_only": True,
}
html_static_path = ["_static"]
html_css_files = ["manual.css"]
html_show_sourcelink = False
html_copy_source = False


def setup(app):
    app.add_lexer("vortexros-cli", TextLexer)
    app.add_lexer("vortexros-config", TextLexer)
