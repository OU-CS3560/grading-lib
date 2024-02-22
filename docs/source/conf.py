# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os

with open(os.path.join(__file__, "VERSION")) as version_file:
    version = version_file.read().strip()

project = "CS3560's Grading Library"
copyright = "2024, Krerkkiat Chusap"
author = "Krerkkiat Chusap"
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "autodoc2"]

templates_path = ["_templates"]
exclude_patterns = []

autodoc2_packages = [
    "../../grading_lib",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
