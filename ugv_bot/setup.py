import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'ugv_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'model'), glob(os.path.join('model', '*.[uxg]*'))),
        (os.path.join('share', package_name, 'parameters'), glob(os.path.join('parameters', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aditya',
    maintainer_email='aditya@todo.todo',
    description='UGV_BOT',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controller_final = ugv_bot.controller_final:main',
        ],
    },
)