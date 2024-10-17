# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os

package_root_dir = os.path.join(os.path.dirname(__file__), "..", "..", "grading_lib")
with open(os.path.join(package_root_dir, "VERSION")) as version_file:
    version = version_file.read().strip()

project = "CS3560's Grading Library"
copyright = "2024, Krerkkiat Chusap"
author = "Krerkkiat Chusap"
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "autodoc2"]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

autodoc2_docstring_parser_regexes = [
    # this will render all docstrings as 'MyST' Markdown
    (r".*", "myst"),
]
autodoc2_render_plugin = "myst"
autodoc2_packages = [
    {
        "path": "../../grading_lib",
        "auto_mode": False,
    },
]

myst_enable_extensions = ["fieldlist"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
# html_static_path = ["_static"]
