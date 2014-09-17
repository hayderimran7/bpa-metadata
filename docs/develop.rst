BPA Metadata Development
========================

**The standard CCG development process applies.**

Workflow is build around the *ccg* workflow tool and *develop.sh*

From scratch
------------

If you don't have the *ccg* tool available then the standard Django development workflow can be used to get the application deployed on a your development machine:
 * Create a virtualenv
 * pip install -e 
 * The *develop.sh* script does not current directly support the creation of a development environment, but it should be fairly straight forward to adapt.
 * Use the ingest scripts to populate the local database, the raw metadata should be available from `BPA Downloads <http://downloads.bioplatforms.com>`_
