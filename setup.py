from setuptools import setup, find_packages

setup(
    name="gglconsole",
    version="0.1",
    url="https://github.com/uezo/gglconsole",
    author="uezo",
    author_email="uezo@uezo.net",
    maintainer="uezo",
    maintainer_email="uezo@uezo.net",
    description="GGLConsole provides you the command line interface for websearch by Google / Bing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    install_requires=["requests", "rich"],
    license="Apache v2",
    entry_points="""
    [console_scripts]
    ggl=gglconsole.gglconsole:main
    bing=gglconsole.gglconsole:main
    qiita=gglconsole.gglconsole:main
    """
)
