from setuptools import setup, find_packages

setup(
    name="gglconsole",
    version="0.2.2",
    url="https://github.com/uezo/gglconsole",
    author="uezo",
    author_email="uezo@uezo.net",
    maintainer="uezo",
    maintainer_email="uezo@uezo.net",
    description="GGLConsole provides you the command line interface for websearch by Google / Bing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*", "resources*"]),
    install_requires=["requests", "rich"],
    license="Apache v2",
    entry_points="""
    [console_scripts]
    ggl=gglconsole:main
    bing=gglconsole:main
    qiita=gglconsole:main
    """
)
