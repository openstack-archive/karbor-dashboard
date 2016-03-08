===============================
smaug-dashboard
===============================

Smaug Dashboard

* Free software: Apache license
* Source: http://git.openstack.org/cgit/openstack/smaug-dashboard
* Bugs: http://bugs.launchpad.net/smaug-dashboard

Installation instructions
-------------------------

Begin by cloning the Horizon and Smaug Dashboard repositories::

    git clone https://git.openstack.org/openstack/horizon
    git clone https://git.openstack.org/openstack/smaug-dashboard

Create a virtual environment and install Horizon dependencies::

    cd horizon
    python tools/install_venv.py

Set up your ``local_settings.py`` file::

    cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

Open up the copied ``local_settings.py`` file in your preferred text
editor. You will want to customize several settings:

-  ``OPENSTACK_HOST`` should be configured with the hostname of your
   OpenStack server. Verify that the ``OPENSTACK_KEYSTONE_URL`` and
   ``OPENSTACK_KEYSTONE_DEFAULT_ROLE`` settings are correct for your
   environment. (They should be correct unless you modified your
   OpenStack server to change them.)


Install Smaug Dashboard with all dependencies in your virtual environment::

    tools/with_venv.sh pip install -e ../smaug-dashboard/

And enable it in Horizon::

    cp ../smaug-dashboard/smaug_dashboard/enabled/_6000_data_protection.py openstack_dashboard/local/enabled
    cp ../smaug-dashboard/smaug_dashboard/enabled/_6010_data_protection_protection_plans_panel.py openstack_dashboard/local/enabled
    cp ../smaug-dashboard/smaug_dashboard/enabled/_6020_data_protection_protection_providers_panel.py openstack_dashboard/local/enabled
    cp ../smaug-dashboard/smaug_dashboard/enabled/_6030_data_protection_checkpoints_panel.py openstack_dashboard/local/enabled
    cp ../smaug-dashboard/smaug_dashboard/enabled/_6040_data_protection_operation_logs_panel.py openstack_dashboard/local/enabled
    cp ../smaug-dashboard/smaug_dashboard/enabled/_6050_data_protection_triggers_panel.py openstack_dashboard/local/enabled

To run horizon with the newly enabled Smaug Dashboard plugin run::

    ./run_tests.sh --runserver 0.0.0.0:8080

to have the application start on port 8080 and the horizon dashboard will be
available in your browser at http://localhost:8080/
