import os

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.exceptions import PluginError
from mkdocs.utils import copy_file

from mkdocs_charts_plugin.fences import fence_vegalite

HERE = os.path.dirname(os.path.abspath(__file__))


CUSTOM_FENCES = [{"name": "vegalite", "class": "vegalite", "format": fence_vegalite}]


def check_library(libnames, dependency):
    for lib in libnames:
        if dependency in lib:
            return True
    raise PluginError(
        f"Missing 'extra_javascript' dependency for {dependency}. Please see setup instructions."
    )


class ChartsPlugin(BasePlugin):

    config_scheme = (
        ("data_path", config_options.Type(str, default="")),
        ("use_data_path", config_options.Type(bool, default=True)),
        ("vega_theme", config_options.Type(str, default="default")),
        ("vega_theme_dark", config_options.Type(str, default="dark")),
        ("vega_renderer", config_options.Type(str, default="svg")),
        ("vega_width", config_options.Type(str, default="container")),
        ("fallback_width", config_options.Type(str, default="800")),
    )

    def on_config(self, config, **kwargs):
        """
        Event trigger on config.
        See https://www.mkdocs.org/user-guide/plugins/#on_config.
        """
        # Add pointer to mkdocs-charts-plugin.js
        # which is added to the output directory during on_post_build() event
        config["extra_javascript"] = ["js/mkdocs-charts-plugin.js"] + config[
            "extra_javascript"
        ]

        # Make sure custom fences are configured.
        custom_fences = (
            config.get("mdx_configs").get("pymdownx.superfences").get("custom_fences")
        )
        if not custom_fences:
            raise PluginError(
                "[mkdocs_charts_plugin]: You have not configured any custom fences, please see the setup instructions."
            )

        # Make sure javascript is configured
        libnames = config.get("extra_javascript", [])
        check_library(libnames, "vega")
        check_library(libnames, "vega-lite")
        check_library(libnames, "vega-embed")

    def on_page_content(self, html, page, config, files, **kwargs):
        """
        Store reference to homepage
        """
        if page.file.src_path == "index.md":
            self.homepage = page.file

    def on_post_page(self, output, page, config, **kwargs):
        """
        Insert plugin config as javascript variables into the page.
        """
        # Early return if not necessary
        if "vegalite" not in output:
            return output

        # Find path to homepage
        path_to_homepage = self.homepage.url_relative_to(page.file)
        path_to_homepage = os.path.dirname(path_to_homepage)
        if config.get("use_directory_urls"):
            path_to_homepage = os.path.join("..", path_to_homepage)
        self.config["path_to_homepage"] = path_to_homepage

        # ensure plugin config is string
        self.config["use_data_path"] = str(self.config["use_data_path"])

        # Config as javascript dictionary
        add_variables = f"""
        <script>
        var mkdocs_chart_plugin = {self.config}
        </script>
        """

        # insert into end of page
        idx = output.index("</body>")
        output = output[:idx] + add_variables + output[idx:]

        return output

    def on_post_build(self, config, **kwargs):
        """
        The post_build event does not alter any variables. Use this event to call post-build scripts.
        See https://www.mkdocs.org/user-guide/plugins/#on_post_build.
        """

        # Add mkdocs-charts-plugin.js
        js_output_base_path = os.path.join(config["site_dir"], "js")
        js_file_path = os.path.join(js_output_base_path, "mkdocs-charts-plugin.js")
        copy_file(
            os.path.join(os.path.join(HERE, "js"), "mkdocs-charts-plugin.js"),
            js_file_path,
        )
