from setuptools import setup, find_packages

setup(
    name="task-manager",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PySide6>=6.5.0",
    ],
    entry_points={
        'console_scripts': [
            'task-manager=src.main:main',
        ],
    },
    author="Marco Yang",
    author_email="marco_yang@msn.com",
    description="A task management application built with PySide6",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="GPL-2.0",
    keywords="task manager, pyside6, qt",
    url="https://github.com/yourusername/task-manager",
    python_requires=">=3.10",
)