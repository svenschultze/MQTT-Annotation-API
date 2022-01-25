from setuptools import setup
from setuptools import find_packages

package_name = 'ros2_annotation_api'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    py_modules=[
        'ros2_annotation_api.ros'
    ],
    install_requires=['setuptools'],
    author='Sven Schultze',
    keywords=['ROS'],
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    license='Apache License, Version 2.0'
)
