If you already have an Odoo instance up and running, your preferred way to install
addons will work with `Business Requirement`.

A reasonable knowledge of Odoo technical management is necessary to be able to
install and run this modules. The
`standard installation how-to <https://www.odoo.com/documentation/12.0/setup/install.html>`_
should be able to get you started.

Using git
~~~~~~~~~
The most common way to install the module is to clone the git repository in your
server and add the directory to your `odoo.conf` file:

#. Clone the git repository

   .. code-block:: sh

      cd your-addons-path
      git clone https://github.com/OCA/business-requirement
      cd business-requirement
      git checkout 12.0 #for the version 12.0

#. Update the addon path of `odoo.conf`
#. Restart Odoo
#. Update the addons list in your database (Menu `Apps > Update Apps List` in developer mode)
#. Install the `Business Requirements` modules in menu `Apps`.

Using pip
~~~~~~~~~
An easy way to install it with all its dependencies is using pip:

#. Recover the code from pip repository

   .. code-block:: sh

      pip install odoo10-addon-business_requirement odoo-autodiscover

#. Restart Odoo
#. Update the addons list in your database (Menu `Apps > Update Apps List` in developer mode)
#. Install the `Business Requirements` modules in menu `Apps`.

Fresh install with Docker
~~~~~~~~~~~~~~~~~~~~~~~~~
If you do not have any Odoo server installed, you can start your own Odoo in few
minutes via Docker in command line.

Here is the basic how-to (based on https://github.com/Elico-Corp/odoo-docker), valid
for Ubuntu OS but could also easily be replicated in MacOS or Windows:

#. Install docker and docker-compose in your system
#. Create the directory structure (assuming the base directory is `odoo`)

   .. code-block:: sh

      mkdir odoo && cd odoo
      mkdir -p ./volumes/postgres ./volumes/odoo/addons ./volumes/odoo/filestore \
      ./volumes/odoo/sessions

#. Create a `docker-compose.yml` file in `odoo` directory with following content:

   .. code-block:: xml

       version: '3.3'
       services:

         postgres:
           image: postgres:9.5
           volumes:
             - ./volumes/postgres:/var/lib/postgresql/data
           environment:
             - POSTGRES_USER=odoo

         odoo:
           image: elicocorp/odoo:12.0
           command: start
           ports:
             - 127.0.0.1:8069:8069
           volumes:
             - ./volumes/odoo/addons:/opt/odoo/additional_addons
             - ./volumes/odoo/filestore:/opt/odoo/data/filestore
             - ./volumes/odoo/sessions:/opt/odoo/data/sessions
           links:
             - postgres:db
           environment:
             - ADDONS_REPO=https://github.com/OCA/business-requirement.git
             - ODOO_DB_USER=odoo

#. Fire up your container (in `odoo` directory)

   .. code-block:: sh

      docker-compose up -d odoo

#. Open a web browser and navigate the URL you have set up in your `docker-compose.yml`
   file (http://127.0.0.1:8069 in this particular example)
#. Create a new database
#. Update the addons list in your database (Menu `Apps > Update Apps List` in developer mode)
#. Install the `Business Requirements` modules in menu `Apps`.

You can improve your new Odoo docker environment (add parameters, change default
passwords etc.) following this `documentation <https://github.com/Elico-Corp/odoo-docker>`_

Now what?
~~~~~~~~~
Check the `Official Documentation <https://www.odoo.com/documentation/12.0>`_ to start using Odoo and developing your own modules.
