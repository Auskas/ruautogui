import os
import re
import setuptools

package_folder = os.path.dirname(os.path.realpath(__file__))
os.chdir(package_folder)

with open('ruautogui/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RuAutoGUI", # Replace with your own username
    version=version,
    author="Dmitry Kudryashov",
    author_email="dmitry-kud@yandex.ru",
    description="RuAutoGUI contols mouse and keyboard in a human-like way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Auskas/ruautogui",
    license='MIT',
    packages=setuptools.find_packages(),
    keywords="gui automation test testing keyboard mouse cursor click press keystroke control",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires='>=3.6',
)