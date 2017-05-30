from setuptools import setup

setup(
    name='Demo Alexa Skill for Dractor',
    version='0.1.0',
    long_description=__doc__,
    packages=['dractor_skill'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'flask-ask',
        'dractor'
    ],
    entry_points={
        'console_scripts': [
            'dractor_skill=dractor_skill.skill:main'
        ]
    }
)
