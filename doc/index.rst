CSV Purchase Import
###################

The csv_purchase module allows to import purchases from csv files.

Configuration
=============

Importing purchases from csv files taken as attachments of emails that are
downloaded automatically via a scheduler, requires additional configuration.
To do this, open the Group menu, select the group "CSV Import Administrator",
and in the tab "Access Permissions" add models "Purchase" and "Purchase Line" with
permission to read, modify, create and delete.
