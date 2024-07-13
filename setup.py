
import setuptools

install_requires = [
    'openai',
    'python-dotenv',
    'colorama'
]

setuptools.setup(
    name='draft-pilot',
    version='0.1',
    author="jon-alamo",
    author_email="jonrivala@gmail.com",
    description="Iterative Human-Supervised Code Assistant",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'draftme = drafter.commands:iterate_draft',
        ],
    },
)
