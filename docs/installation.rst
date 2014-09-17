Installation
============

**The standard CCG rpm installation process applies:**

 * Build a rpm, using develop.sh ccg directly or in the lxc container.
 * Staging
    * Push rpm to staging repository.
    * Deploy on staging
    * Run ingest script on staging.
 * Production
    * Publish vetted rpm to production repository.
    * Install on production VM.
    * Run ingest script on production.


Deployment
----------

The standard ccg assisted deployment to AWS EC2 applies.