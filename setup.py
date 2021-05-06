"""
# Details ---------------------------------------------------------------
#       AUTHOR:	Benjamin Wild       DATE: 2018 07 16
#     MODIFIED:	James Foster        DATE: 2021 05 06
#
#  DESCRIPTION: Setup for bb_wdd2.
#               
#      OUTPUTS: Parameters.
#
#	   CHANGES: -Updated names for requirements and URLs
#
#   REFERENCES: Wario, F., Wild, B., Rojas, R., Landgraf, T., 2017.
#               Automatic detection and decoding of honey bee waggle dances. 
#               PLoS ONE 12, 1–16. 
#               https://doi.org/10.1371/journal.pone.0188626
# 
#TODO   
#- Test run  
#- Fix camera setup?     

"""
from distutils.core import setup
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
#reqs = [str(ir.req) for ir in install_reqs]
reqs = [str(ir.requirement) for ir in install_reqs]
#dep_links = [str(req_line.url) for req_line in install_reqs]
dep_links = [str(req_line.line_source) for req_line in install_reqs]

setup(
    name='bb_wdd',
    version='2.0.0',
    description='',
    entry_points={
        'console_scripts': [
            'bb_wdd = wdd.scripts.bb_wdd:main',
        ]
    },
    install_requires=reqs,
    dependency_links=dep_links,
    extras_require={
        'Flea3': ['PyCapture2'],
    },
    packages=[
        'wdd',
        'wdd.scripts',
    ],
)
