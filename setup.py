from distutils.core import setup

setup(
    name='emulambda',
    version='0.0',
    packages=['emulambda'],
    scripts=['bin/emulambda'],
    url='http://www.fugue.co',
    license='Apache 2.0',
    author='dominiczippilli',
    author_email='dom@fugue.co',
    description='Python emulator for AWS Lambda.',
    install_requires=[
        'hurry.filesize',
        'boto3',
        'nose'
      ]
)
