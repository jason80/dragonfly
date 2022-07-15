from setuptools import setup

setup(
    name='dragonfly-ifl',
    version='0.0.1',    
    description='An interactive fiction and adventure games library',
    url='https://github.com/jason80/dragonfly',
    author='Javier Candales (Jasoón)',
    author_email='javier_candales@yahoo.com.ar',
    license='GPL',
    packages=['dragonfly', 'dragonfly.output', 'dragonfly.syntax', 'dragonfly.helper'],
    install_requires=['PyQt5',                     
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
		'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  
        'Operating System :: POSIX :: Linux',
		'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
		'Topic :: Games/Entertainment'
    ],
)
