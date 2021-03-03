from setuptools import setup, find_namespace_packages


setup(
    name="project_creator",
    version="0.0.1",
    python_requires=">=3.6",
    packages=find_namespace_packages(include=["project_creator*"]),
    install_requires=["requests>=2.25.1"],
    dependency_links=[
        "https://pypi.org/project/requests/",
    ],
    entry_points={
        'console_scripts': ['project_creator = project_creator.main:main'],
    },
)
